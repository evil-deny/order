import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {plannedQuantity,shippedQuantity} from '../assets/fulfillment.js';
test('預設、部分出貨及舊版訂單數量相容',()=>{
 assert.equal(plannedQuantity({qty:5,picked:true,pickQty:5}),5);assert.equal(plannedQuantity({qty:5,picked:true,pickQty:3}),3);assert.equal(shippedQuantity({qty:5,shippedQty:3}),3);assert.equal(shippedQuantity({qty:5,picked:true}),5);assert.equal(shippedQuantity({qty:5,picked:false}),0);
});
test('快速連續變更實際數量會依序保存，不會被忙碌狀態略過',async()=>{
 const html=readFileSync(new URL('../index.html',import.meta.url),'utf8'),start=html.indexOf('    let cloudActionQueue='),end=html.indexOf("    document.addEventListener('click',e=>{",start),calls=[];
 const context={cloudBusy:false,refreshCloud:async()=>calls.push('refresh'),FuyuanCloud:{notice:()=>{}},Promise};
 vm.runInNewContext(html.slice(start,end),context);
 await Promise.all([context.cloudAction(async()=>{await Promise.resolve();calls.push(1);}),context.cloudAction(async()=>calls.push(2)),context.cloudAction(async()=>calls.push(3))]);assert.deepEqual(calls,[1,'refresh',2,'refresh',3,'refresh']);assert.equal(context.cloudBusy,false);
});
test('出貨頁預設全數，重讀保存數量可顯示三件',()=>{
 const html=readFileSync(new URL('../index.html',import.meta.url),'utf8'),start=html.indexOf('    function shippingQuantities('),end=html.indexOf('    function returnedQty(',start),target={innerHTML:''};
 const item={id:'p1',name:'商品',qty:5,price:40,pickQty:5,picked:true,unit:'包'},state={orders:[{id:'o1',name:'測試',status:'new',createdAt:'test',items:[item]}]};
 const ctx={state,plannedQuantity,document:{getElementById:()=>target},attrText:s=>s,itemName:i=>i.name,itemUnit:i=>i.unit,itemPrice:i=>i.price,money:n=>'$'+n,orderLabel:s=>s,sourceLabel:()=>'',sourceClass:()=>'',statusText:()=>''};vm.runInNewContext(html.slice(start,end),ctx);
 ctx.renderShipping();assert.match(target.innerHTML,/max="5"/);assert.match(target.innerHTML,/value="5"/);assert.match(target.innerHTML,/checked/);item.pickQty=3;ctx.renderShipping();assert.match(target.innerHTML,/value="3"/);
});
