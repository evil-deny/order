import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {receiptShareGroups,receiptSections,receiptCategory} from '../assets/receipt-share.js';
const items=[{id:'company',name:'公司商品',category:'公司庫存',unit:'5斤',qty:2,price:100},{id:'two',name:'兩天商品',category:'兩天一次(三五日結單/一四六到貨)',qty:3,price:50},{id:'daily',name:'白豆腐',category:'每日叫貨',qty:1,price:210},{id:'fee-rent',name:'租金位子',custom:true,category:'額外費用',qty:1,price:500}];
test('額外檢貨單只含兩天一次，完整單保持原樣；沒有時不產生空單',()=>{
 const groups=receiptShareGroups({items});assert.equal(groups.length,2);assert.deepEqual(groups[0].items,items);assert.deepEqual(groups[1].items,[items[1]]);assert.equal(groups[1].title,'兩天一次檢貨單');
 assert.equal(receiptShareGroups({items:items.filter(i=>i.id!=='two')}).length,1);
 assert.equal(receiptShareGroups({items:[{id:'old'}]},()=> '兩天一次').length,2);
 assert.equal(receiptShareGroups({items:[{id:'custom',custom:true,category:'兩天一次'}]}).length,1);
});
test('分享兩張圖片只送出一筆訂單，重試不重複送單',async()=>{
 const html=readFileSync(new URL('../index.html',import.meta.url),'utf8'),start=html.indexOf('    async function shareReceiptImage(){'),end=html.indexOf('    function syncPendingToPage()',start);
 let submits=0,shares=[],closed=0;const button={disabled:false},pendingOrder={name:'測試',items};
 const context={pendingOrder,receiptShareGroups,Date,File,URL,alert:()=>{},document:{getElementById:()=>button},product:id=>items.find(i=>i.id===id),submitPendingOrder:async()=>{if(!pendingOrder.cloudSubmitted){submits++;pendingOrder.cloudSubmitted={id:'one-order'};}},drawShareCanvas:(lines,title)=>({toBlob:fn=>fn(new Blob([JSON.stringify({title,ids:lines.map(i=>i.id)})],{type:'image/png'}))}),navigator:{canShare:({files})=>files.length===2,share:async payload=>shares.push(payload)},closeModal:()=>closed++};
 vm.runInNewContext(html.slice(start,end),context);await context.shareReceiptImage();await context.shareReceiptImage();
 assert.equal(submits,1);assert.equal(shares.length,2);assert.equal(shares[0].files.length,2);assert.match(shares[0].files[1].name,/兩天一次檢貨單/);assert.deepEqual(JSON.parse(await shares[0].files[1].text()).ids,['two']);assert.equal(closed,2);assert.equal(button.disabled,false);
});
test('兩張圖片沿用完整高度計算，額外單只計該類商品金額',()=>{
 const html=readFileSync(new URL('../index.html',import.meta.url),'utf8'),start=html.indexOf('    function canvasTextLines('),end=html.indexOf('    async function shareReceiptImage()',start),canvases=[];
 const context={receiptSections,product:id=>items.find(i=>i.id===id),pendingOrder:{name:'測試',note:'有備註',createdAt:'11/27 12:00',items},itemName:i=>i.name,itemPrice:i=>i.price,itemSubtotal:i=>i.qty*i.price,money:n=>'$'+n,document:{createElement:()=>{const drawn=[],rects=[],ctx={measureText:t=>({width:t.length*26}),fillRect:(x,y,w,h)=>rects.push([y,h]),strokeRect:(x,y,w,h)=>rects.push([y,h]),fillText:(text,x,y)=>drawn.push({text,y}),beginPath(){},moveTo(){},lineTo(){},stroke(){}};const canvas={width:0,height:0,drawn,rects,getContext:()=>ctx};canvases.push(canvas);return canvas;}}};
 vm.runInNewContext(html.slice(start,end),context);
 const full=context.drawShareCanvas(),extra=context.drawShareCanvas([items[1]],'兩天一次檢貨單');
 for(const category of ['公司庫存','兩天一次','每日叫貨','額外費用'])assert(full.drawn.some(r=>r.text===category));assert(extra.drawn.some(r=>r.text==='兩天一次'));assert(!extra.drawn.some(r=>r.text==='公司庫存'));assert(full.drawn.some(r=>r.text==='2 / 5斤'));assert(full.drawn.some(r=>r.text==='總金額：$1060'));assert(extra.drawn.some(r=>r.text==='總金額：$150'));assert(!extra.drawn.some(r=>r.text==='白豆腐'));assert(extra.rects.slice(1).every(([y,h])=>y+h<=extra.height-39));assert(full.rects.slice(1).every(([y,h])=>y+h<=full.height-39));
});

test('分類依四大分類排序並保留原明細索引，舊費用及自訂品項不誤分',()=>{
 const scrambled=[items[3],items[2],items[0],items[1]],sections=receiptSections(scrambled);
 assert.deepEqual(sections.map(s=>s.category),['公司庫存','兩天一次','每日叫貨','額外費用']);
 assert.deepEqual(sections.map(s=>s.entries[0].index),[2,3,1,0]);assert.equal(receiptCategory({id:'fee-rent',custom:true},()=> '已刪除'),'額外費用');assert.equal(receiptCategory({id:'custom',custom:true},()=> '已刪除'),'客製化品項');
});
test('確認畫面與列印明細都有分類列，品項編輯仍指向原始索引',()=>{
 const html=readFileSync(new URL('../index.html',import.meta.url),'utf8'),start=html.indexOf('    function drawReceipt(){'),end=html.indexOf('    function canvasTextLines(',start),target={innerHTML:''};
 const ctx={receiptSections,pendingOrder:{name:'測試',createdAt:'11/27',items:[items[3],items[2],items[0],items[1]]},document:{querySelector:()=>({textContent:''}),querySelectorAll:()=>[],getElementById:()=>target},attrText:s=>String(s),isExtraFee:i=>i.id==='fee-rent',itemName:i=>i.name,itemUnit:i=>i.unit||'件',itemPrice:i=>i.price,itemSubtotal:i=>i.qty*i.price,money:n=>'$'+n,product:()=>null};
 vm.runInNewContext(html.slice(start,end),ctx);ctx.drawReceipt();
 assert.equal((target.innerHTML.match(/class="receipt-category"/g)||[]).length,8);assert.match(target.innerHTML,/data-receipt-inc="2"/);assert.match(target.innerHTML,/總金額/);assert(target.innerHTML.includes('2 / 5斤'));
});
