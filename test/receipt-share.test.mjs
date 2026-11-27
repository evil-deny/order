import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {receiptShareGroups} from '../assets/receipt-share.js';
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
 const context={pendingOrder:{name:'測試',note:'有備註',createdAt:'11/27 12:00',items},itemName:i=>i.name,itemPrice:i=>i.price,itemSubtotal:i=>i.qty*i.price,money:n=>'$'+n,document:{createElement:()=>{const drawn=[],rects=[],ctx={measureText:t=>({width:t.length*26}),fillRect:(x,y,w,h)=>rects.push([y,h]),strokeRect:(x,y,w,h)=>rects.push([y,h]),fillText:(text,x,y)=>drawn.push({text,y}),beginPath(){},moveTo(){},lineTo(){},stroke(){}};const canvas={width:0,height:0,drawn,rects,getContext:()=>ctx};canvases.push(canvas);return canvas;}}};
 vm.runInNewContext(html.slice(start,end),context);
 const full=context.drawShareCanvas(),extra=context.drawShareCanvas([items[1]],'兩天一次檢貨單');
 assert(full.drawn.some(r=>r.text==='2 / 5斤'));assert(full.drawn.some(r=>r.text==='總金額：$1060'));assert(extra.drawn.some(r=>r.text==='總金額：$150'));assert(!extra.drawn.some(r=>r.text==='白豆腐'));assert(extra.rects.slice(1).every(([y,h])=>y+h<=extra.height-39));assert(full.rects.slice(1).every(([y,h])=>y+h<=full.height-39));
});
