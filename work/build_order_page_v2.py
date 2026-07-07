from pathlib import Path
import json

products = json.loads(Path("work/products.json").read_text(encoding="utf-8"))
products_json = json.dumps(products, ensure_ascii=False)

html = r'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>福緣訂單系統</title>
  <style>
    :root {
      --bg:#f5f7fa; --card:#fff; --ink:#1f2937; --muted:#64748b; --line:#d8e0ea;
      --main:#0f766e; --blue:#2563eb; --red:#dc2626; --amber:#b45309;
      --shadow:0 10px 24px rgba(15,23,42,.08);
      font-family:"Microsoft JhengHei","Noto Sans TC",system-ui,sans-serif;
    }
    *{box-sizing:border-box}
    body{margin:0;background:var(--bg);color:var(--ink);font-size:18px;letter-spacing:0}
    button,input,select{font:inherit}
    button{border:0;border-radius:8px;cursor:pointer;font-weight:800}
    .topbar{position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px clamp(12px,3vw,28px);background:#fff;border-bottom:1px solid var(--line);box-shadow:0 2px 10px rgba(15,23,42,.05)}
    .brand{display:flex;align-items:center;gap:10px;min-width:0}
    .brand img{width:56px;height:56px;object-fit:cover;border-radius:8px;border:1px solid var(--line);background:#fff}
    .brand strong{display:block;font-size:26px;line-height:1.1}.brand span{display:block;color:var(--muted);font-size:16px;margin-top:3px}
    .admin-open,.secondary{min-height:48px;padding:0 16px;background:#e8eef5;color:#243244}
    .wrap{max-width:1120px;margin:0 auto;padding:14px 12px 116px}
    .box,.category,.custom-panel{background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:var(--shadow)}
    .customer-box{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:10px;padding:12px;margin-bottom:12px}
    label{display:grid;gap:6px;color:var(--muted);font-size:17px;font-weight:800}
    input,select{width:100%;min-height:52px;padding:12px 14px;border:1px solid var(--line);border-radius:8px;color:var(--ink);background:#fff;outline:none;font-size:19px}
    input:focus,select:focus{border-color:var(--main);box-shadow:0 0 0 3px rgba(15,118,110,.12)}
    .custom-panel{padding:12px;margin-bottom:12px}
    .main-tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:12px}
    .main-tab{min-height:54px;background:#e2e8f0;color:#243244;font-size:21px}
    .main-tab.active{background:var(--main);color:#fff}
    .main-view{display:none}.main-view.active{display:block}
    .custom-grid{display:grid;grid-template-columns:minmax(0,1.5fr) 120px 100px auto;gap:8px;align-items:end}
    .custom-list{display:grid;gap:8px;margin-top:10px}
    .search-row{position:sticky;top:69px;z-index:15;display:grid;grid-template-columns:minmax(0,1fr) 150px;gap:10px;padding:10px 0;background:var(--bg)}
    .category{margin-top:14px;overflow:hidden}.category-title{display:flex;justify-content:space-between;align-items:center;padding:14px;background:#eef5f5;border-bottom:1px solid var(--line);font-size:23px;font-weight:900}
    .category-count{color:var(--muted);font-size:17px;font-weight:700}.items{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:10px}
    .item{display:grid;grid-template-columns:82px minmax(0,1fr);gap:10px;padding:10px;border:1px solid var(--line);border-radius:9px;background:#fff}
    .item img{width:82px;height:82px;object-fit:cover;border-radius:8px;border:1px solid var(--line);background:#f1f5f9}.item h3{margin:0;font-size:21px;line-height:1.35;word-break:break-word}
    .meta{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:7px 0 10px;color:var(--muted);font-size:16px;font-weight:700}.price{color:var(--red);font-size:20px}.stock{color:var(--amber);background:#fff7ed;padding:2px 7px;border-radius:99px}
    .qty{display:grid;grid-template-columns:46px minmax(54px,1fr) 46px;gap:7px;align-items:center}.qty button{width:46px;height:46px;background:#e2e8f0;color:#243244;font-size:24px}.qty input{min-height:46px;text-align:center;padding:4px;font-size:24px;font-weight:900}
    .bottom-bar{position:fixed;left:0;right:0;bottom:0;z-index:25;display:flex;justify-content:center;padding:10px 12px;background:rgba(255,255,255,.96);border-top:1px solid var(--line);box-shadow:0 -8px 24px rgba(15,23,42,.08)}
    .bottom-inner{width:min(1120px,100%);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center}.total{font-size:18px;color:var(--muted);font-weight:800}.total strong{display:block;color:var(--red);font-size:34px;line-height:1.05}
    .checkout,.primary{min-height:52px;padding:0 18px;background:var(--main);color:#fff}.checkout{min-height:62px;font-size:22px}.danger{min-height:48px;padding:0 15px;background:var(--red);color:#fff}.blue{min-height:48px;padding:0 15px;background:var(--blue);color:#fff}
    .modal{display:none;position:fixed;inset:0;z-index:50;background:rgba(15,23,42,.55);padding:12px;align-items:center;justify-content:center}.modal.show{display:flex}.modal-card{width:min(980px,100%);max-height:92vh;overflow:auto;background:#fff;border-radius:12px;box-shadow:0 24px 60px rgba(15,23,42,.25)}
    .modal-head{position:sticky;top:0;z-index:2;display:flex;justify-content:space-between;align-items:center;gap:10px;padding:14px 16px;background:#fff;border-bottom:1px solid var(--line)}.modal-head h2{margin:0;font-size:21px}.close{width:40px;height:40px;background:#e2e8f0}
    .modal-body{padding:16px}.line{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;padding:10px;border:1px solid var(--line);border-radius:8px;background:#f8fafc}.line-actions{display:flex;gap:6px;align-items:center;justify-content:flex-end}.line-actions button{width:36px;height:36px;background:#e2e8f0}.line-actions .remove{background:#fee2e2;color:#991b1b;width:auto;padding:0 10px}.receipt-list,.pick-list{display:grid;gap:8px;margin:12px 0}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
    .admin-tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:14px}.tab{min-height:52px;background:#e2e8f0;color:#243244}.tab.active{background:var(--main);color:#fff}.admin-view{display:none}.admin-view.active{display:block}
    .metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-bottom:14px}.metric{padding:14px;border:1px solid var(--line);border-radius:10px;background:#f8fafc}.metric span{color:var(--muted);font-size:13px;font-weight:800}.metric strong{display:block;margin-top:7px;font-size:25px}
    .order-card,.inventory-row{display:grid;gap:10px;padding:12px;margin-bottom:10px;border:1px solid var(--line);border-radius:10px;background:#fff}.order-title{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;font-weight:900}.badge{display:inline-flex;align-items:center;min-height:26px;padding:2px 9px;border-radius:99px;background:#dbeafe;color:#1d4ed8;font-size:13px;font-weight:900}.badge.shipped{background:#dcfce7;color:#166534}.badge.returned{background:#fee2e2;color:#991b1b}.badge.done{background:#dcfce7;color:#166534}
    .check{display:grid;grid-template-columns:24px minmax(0,1fr) auto;gap:8px;align-items:center;padding:9px;border:1px solid var(--line);border-radius:8px;background:#f8fafc}.check input{width:20px;min-height:20px;accent-color:var(--main)}
    .return-grid{display:grid;gap:8px}.return-line{display:grid;grid-template-columns:24px minmax(0,1fr) 90px;gap:8px;align-items:center;padding:9px;border:1px solid var(--line);border-radius:8px;background:#f8fafc}.return-line input[type=checkbox]{width:20px;min-height:20px}.inventory-row{grid-template-columns:minmax(0,1.4fr) 110px 110px 140px 180px;align-items:center}.stock-controls{display:grid;grid-template-columns:42px minmax(55px,1fr) 42px;gap:6px}.stock-controls button{width:42px;height:42px;background:#e2e8f0}.stock-controls input{text-align:center;font-weight:900;padding:4px}
    .empty{padding:24px;color:var(--muted);text-align:center;border:1px dashed var(--line);border-radius:10px;background:#f8fafc}
    @media print{
      body{background:#fff}
      .topbar,.wrap,.bottom-bar,.modal:not(#receiptModal),#receiptModal .modal-head,#receiptModal .actions{display:none!important}
      #receiptModal{display:block!important;position:static;background:#fff;padding:0}
      #receiptModal .modal-card{width:100%;max-height:none;overflow:visible;box-shadow:none;border-radius:0}
      #receiptModal .modal-body{padding:0}
      #receiptContent{padding:12px;color:#000}
      .line{break-inside:avoid;background:#fff;border-color:#999}
      .screen-receipt{display:none!important}
      .print-receipt{display:block!important}
      .print-table{width:100%;border-collapse:collapse;margin-top:14px;font-size:16px}
      .print-table th,.print-table td{border:1px solid #333;padding:8px;text-align:left}
      .print-table th{background:#eee}
      .print-table td:nth-child(2),.print-table td:nth-child(3),.print-table td:nth-child(4),.print-table th:nth-child(2),.print-table th:nth-child(3),.print-table th:nth-child(4){text-align:right}
      .print-total{font-size:24px;font-weight:bold;text-align:right;margin-top:14px;padding:10px;border:2px solid #111}
    }
    .receipt-card{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:#fff}
    .table-wrap{overflow-x:auto}
    .receipt-title{padding:16px;background:#eef5f5;text-align:center}
    .receipt-title h3{margin:0;font-size:24px}
    .receipt-info{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;padding:14px;border-bottom:1px solid var(--line)}
    .receipt-info div{padding:9px 10px;background:#f8fafc;border-radius:8px}
    .receipt-table{width:100%;border-collapse:collapse}
    .receipt-table th,.receipt-table td{padding:11px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
    .receipt-table th{background:#f8fafc;color:var(--muted);font-size:13px}
    .receipt-table td:nth-child(2),.receipt-table td:nth-child(3),.receipt-table td:nth-child(4),.receipt-table th:nth-child(2),.receipt-table th:nth-child(3),.receipt-table th:nth-child(4){text-align:right;white-space:nowrap}
    .receipt-edit{display:flex;gap:6px;justify-content:flex-end;flex-wrap:wrap;margin-top:6px}
    .receipt-edit button{width:34px;height:34px;background:#e2e8f0}
    .receipt-edit .remove{width:auto;padding:0 10px;background:#fee2e2;color:#991b1b}
    .receipt-total-row{display:flex;justify-content:space-between;gap:18px;align-items:center;margin:14px;padding:14px 16px;font-size:24px;font-weight:900;background:#fff7ed;border:2px solid #f59e0b;border-radius:10px;color:#9a3412}
    @media(max-width:760px){.topbar{padding:12px;align-items:flex-start}.brand img{width:48px;height:48px}.brand strong{font-size:22px}.wrap{padding-bottom:132px}.customer-box,.search-row,.items,.bottom-inner,.metrics,.inventory-row,.custom-grid,.receipt-info{grid-template-columns:1fr}.search-row{top:65px}.main-tabs{grid-template-columns:1fr}.item{grid-template-columns:76px minmax(0,1fr);padding:9px}.item img{width:76px;height:76px}.item h3{font-size:20px}.checkout{width:100%}.admin-tabs{grid-template-columns:1fr}.modal-body{padding:12px}.line{grid-template-columns:1fr}.line-actions{justify-content:flex-start}.return-line{grid-template-columns:24px minmax(0,1fr)}.receipt-table th:nth-child(2),.receipt-table td:nth-child(2){display:none}.receipt-table th,.receipt-table td{padding:9px 8px}}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand"><img src="assets/logo.jpg" alt="福緣素食 logo"><div><strong>福緣訂單系統</strong><span>輸入大名，選品項，確認後送出</span></div></div>
    <button class="admin-open" id="openAdmin">後台</button>
  </header>

  <main class="wrap">
    <div class="main-tabs">
      <button class="main-tab active" data-main-view="orderPage">訂購</button>
      <button class="main-tab" data-main-view="shipPage">出貨</button>
      <button class="main-tab" data-main-view="returnPage">退貨</button>
    </div>

    <section class="main-view active" id="orderPage">
      <section class="box customer-box">
        <label>大名<input id="customerName" autocomplete="name" placeholder="請輸入大名"></label>
        <label>備註<input id="customerNote" placeholder="例：不要辣、分開裝、晚點取"></label>
      </section>

      <section class="custom-panel">
        <strong>客製化品項</strong>
        <div class="custom-grid" style="margin-top:10px">
          <label>品名<input id="customName" placeholder="例：代購商品、特別組合"></label>
          <label>單價<input id="customPrice" type="number" min="0" inputmode="numeric" placeholder="0"></label>
          <label>數量<input id="customQty" type="number" min="1" inputmode="numeric" value="1"></label>
          <button class="blue" id="addCustom">新增</button>
        </div>
        <div class="custom-list" id="customList"></div>
      </section>

      <section class="search-row">
        <input id="search" type="search" placeholder="搜尋品項名稱">
        <select id="categoryFilter" aria-label="分類篩選"></select>
      </section>
      <div id="productList"></div>
    </section>

    <section class="main-view" id="shipPage"></section>
    <section class="main-view" id="returnPage"></section>
  </main>

  <footer class="bottom-bar"><div class="bottom-inner"><div class="total">合計 <strong id="cartTotal">$0</strong></div><button class="checkout" id="checkout">確認訂單</button></div></footer>

  <section class="modal" id="receiptModal"><div class="modal-card"><div class="modal-head"><h2>訂單確認</h2><button class="close" data-close="receiptModal">×</button></div><div class="modal-body"><div id="receiptContent"></div><div class="actions"><button class="secondary" data-close="receiptModal">返回修改</button><button class="blue" id="printReceipt">影印明細</button><button class="blue" id="shareReceiptImage">圖片分享</button><button class="primary" id="saveOrder">送出訂單</button></div></div></div></section>
  <section class="modal" id="adminLogin"><div class="modal-card" style="max-width:420px"><div class="modal-head"><h2>後台登入</h2><button class="close" data-close="adminLogin">×</button></div><div class="modal-body"><label>密碼<input id="adminPassword" type="password" inputmode="numeric" placeholder="請輸入密碼"></label><div class="actions"><button class="primary" id="loginAdmin">進入後台</button></div></div></div></section>
  <section class="modal" id="adminPanel"><div class="modal-card"><div class="modal-head"><h2>後台管理</h2><button class="close" data-close="adminPanel">×</button></div><div class="modal-body"><div class="admin-tabs"><button class="tab active" data-admin-tab="overview">總覽</button><button class="tab" data-admin-tab="dailySummary">日品項統計</button><button class="tab" data-admin-tab="inventory">庫存</button></div><div class="admin-view active" id="overview"></div><div class="admin-view" id="dailySummary"></div><div class="admin-view" id="inventory"></div></div></div></section>

  <script>
    const PRODUCTS = __PRODUCTS__;
    const PASSWORD = "0000";
    const STORE_KEY = "clearOrderSystemV3";
    const PLACEHOLDER = "https://via.placeholder.com/120x120?text=No+Image";
    const state = loadState();
    let standardCart = {};
    let customCart = [];
    let pendingOrder = null;

    function loadState(){
      const saved = localStorage.getItem(STORE_KEY);
      if(saved) return JSON.parse(saved);
      return { orders: [], stock: Object.fromEntries(PRODUCTS.map(p => [p.id, p.stock === null ? null : p.stock])) };
    }
    function saveState(){ localStorage.setItem(STORE_KEY, JSON.stringify(state)); }
    function money(v){ return "$" + Number(v || 0).toLocaleString("zh-TW"); }
    function nowText(){ return new Date().toLocaleString("zh-TW",{hour12:false,month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit"}); }
    function dateKey(date){ return date.toISOString().slice(0,10); }
    function orderDate(order){ return order.createdAtISO ? new Date(order.createdAtISO) : new Date(); }
    function product(id){ return PRODUCTS.find(p => p.id === id); }
    function itemName(item){ return item.custom ? item.name : product(item.id).name; }
    function itemPrice(item){ return item.custom ? Number(item.price) : product(item.id).price; }
    function itemSubtotal(item){ return itemPrice(item) * item.qty; }
    function openModal(id){ document.getElementById(id).classList.add("show"); }
    function closeModal(id){ document.getElementById(id).classList.remove("show"); }

    function cartItems(){
      const standard = PRODUCTS.map(p => ({id:p.id, qty:Number(standardCart[p.id] || 0), custom:false})).filter(i => i.qty > 0);
      return [...standard, ...customCart.map(i => ({...i}))];
    }
    function orderTotal(order){ return order.items.reduce((sum,i)=>sum+itemSubtotal(i),0); }
    function returnedTotal(order){ return (order.returns||[]).reduce((sum,i)=>sum+itemSubtotal(i),0); }
    function soldQty(productId){
      return state.orders.reduce((sum,o)=>{
        if(o.status!=="shipped" && o.status!=="returned") return sum;
        const sold=o.items.filter(i=>!i.custom && i.id===productId).reduce((n,i)=>n+i.qty,0);
        const ret=(o.returns||[]).filter(i=>!i.custom && i.id===productId).reduce((n,i)=>n+i.qty,0);
        return sum+sold-ret;
      },0);
    }
    function statusText(s){ return {new:"待出貨",picking:"揀貨中",shipped:"已出貨",returned:"已退貨"}[s] || s; }
    function makeOrderId(name){ return `${name}-${new Date().toISOString().slice(2,10).replaceAll("-","")}-${String(state.orders.length+1).padStart(3,"0")}`; }
    function productType(product){
      const name=product.name;
      const category=product.category || "";
      if(/鬆/.test(name)) return "素鬆/鬆類";
      if(/[湯鍋羹]|四神|麻辣燙/.test(name)) return "湯品/鍋物";
      if(/豆腐|豆包|豆干|豆皮|百頁|腐竹|油泡|干絲|花干|三角|四角|豆漿|豆腱/.test(name)) return "豆製品";
      if(/丸|貢丸|火鍋料|花球|蟹球|絲丸|獅子頭/.test(name)) return "丸類/火鍋料";
      if(/排|肉|雞|鵝|腿|蹄|培根|火腿|香腸|腸|燻|素肚|素雞|植物肉|三牲|腰花/.test(name)) return "素肉/調理肉品";
      if(/魚|蝦|花枝|鮑|干貝|鱈|鮭|海味|烏魚子|鰻/.test(name)) return "海味/魚蝦類";
      if(/菇|菜|筍|蓮|藕|薑|香菜|木瓜|木耳|苦瓜|毛豆|海帶|牛蒡|雪裡紅|菜脯|珊瑚草/.test(name)) return "蔬菜/菇類";
      if(/醬|油|蠔油|香油|米豆|剝皮辣椒|花生麵筋|罐|黃金|鹹魚/.test(name)) return "醬料/罐頭小菜";
      if(/袋|盒|瓶|橡皮筋|束繩|包材|透明|花袋/.test(name) || category.includes("公司庫存") && product.price===0) return "包材/耗材";
      if(/糕|餅|卷|瓜子|點心|抓餅/.test(name)) return "糕餅/點心";
      if(/麵|鐵板/.test(name)) return "麵食";
      if(category.includes("公司庫存")) return "公司庫存其他";
      return "其他訂購品";
    }
    function setMainView(id){
      document.querySelectorAll(".main-tab").forEach(b=>b.classList.toggle("active",b.dataset.mainView===id));
      document.querySelectorAll(".main-view").forEach(v=>v.classList.toggle("active",v.id===id));
      document.querySelector(".bottom-bar").style.display = id==="orderPage" ? "flex" : "none";
      if(id==="shipPage") renderShipping();
      if(id==="returnPage") renderReturns();
    }

    function initFilters(){
      const categories=["全部分類",...new Set(PRODUCTS.map(p=>productType(p)))];
      document.getElementById("categoryFilter").innerHTML=categories.map(c=>`<option value="${c}">${c}</option>`).join("");
    }
    function visibleProducts(){
      const keyword=document.getElementById("search").value.trim().toLowerCase();
      const cat=document.getElementById("categoryFilter").value;
      return PRODUCTS.filter(p => p.name.toLowerCase().includes(keyword) && (cat==="全部分類" || productType(p)===cat));
    }
    function renderProducts(){
      const grouped=new Map();
      visibleProducts().forEach(p=>{ const type=productType(p); if(!grouped.has(type)) grouped.set(type,[]); grouped.get(type).push(p); });
      document.getElementById("productList").innerHTML=[...grouped.entries()].map(([category,items])=>`
        <section class="category"><div class="category-title"><span>${category}</span><span class="category-count">${items.length} 項</span></div><div class="items">
        ${items.map(p=>`<article class="item"><img src="${p.image||PLACEHOLDER}" alt="${p.name}" loading="lazy" onerror="this.src='${PLACEHOLDER}'"><div><h3>${p.name}</h3><div class="meta"><span class="price">單價 ${money(p.price)}</span>${state.stock[p.id]===null?"":`<span class="stock">庫存 ${state.stock[p.id]}</span>`}</div><div class="qty"><button type="button" data-minus="${p.id}">−</button><input id="qty-${p.id}" type="number" min="0" value="${standardCart[p.id] || 0}" inputmode="numeric" data-qty="${p.id}"><button type="button" data-plus="${p.id}">＋</button></div></div></article>`).join("")}
        </div></section>`).join("") || `<div class="empty">找不到品項。</div>`;
      updateTotal();
    }
    function renderCustomList(){
      document.getElementById("customList").innerHTML = customCart.map(item=>`
        <div class="line"><span>${item.name} · 單價 ${money(item.price)} × ${item.qty}</span><span class="line-actions"><button data-custom-dec="${item.id}">−</button><button data-custom-inc="${item.id}">＋</button><button class="remove" data-custom-remove="${item.id}">刪除</button></span></div>
      `).join("");
      updateTotal();
    }
    function updateTotal(){
      document.getElementById("cartTotal").textContent = money(cartItems().reduce((sum,i)=>sum+itemSubtotal(i),0));
    }
    function setQty(id, qty){
      const stock=state.stock[id];
      let next=Math.max(0,Number(qty||0));
      if(stock!==null) next=Math.min(next,stock);
      if(next > 0) standardCart[id]=next;
      else delete standardCart[id];
      const input=document.getElementById("qty-"+id);
      if(input) input.value=next;
      updateTotal();
    }

    function renderReceipt(){
      pendingOrder = { name:document.getElementById("customerName").value.trim(), note:document.getElementById("customerNote").value.trim(), items:cartItems(), createdAt:nowText(), createdAtISO:new Date().toISOString() };
      drawReceipt();
    }
    function drawReceipt(){
      const total=pendingOrder.items.reduce((sum,i)=>sum+itemSubtotal(i),0);
      document.getElementById("receiptContent").innerHTML=`
        <div class="screen-receipt">
          <div class="receipt-card">
            <div class="receipt-title"><h3>福緣訂單明細</h3></div>
            <div class="receipt-info">
              <div><strong>大名</strong><br>${pendingOrder.name}</div>
              <div><strong>開單時間</strong><br>${pendingOrder.createdAt}</div>
              ${pendingOrder.note?`<div style="grid-column:1/-1"><strong>備註</strong><br>${pendingOrder.note}</div>`:""}
            </div>
            <table class="receipt-table">
              <thead><tr><th>商品</th><th>單價</th><th>數量</th><th>小計</th></tr></thead>
              <tbody>${pendingOrder.items.map((item,index)=>`<tr><td><strong>${itemName(item)}</strong><div class="receipt-edit"><button data-receipt-dec="${index}">−</button><button data-receipt-inc="${index}">＋</button><button class="remove" data-receipt-remove="${index}">刪除</button></div></td><td>${money(itemPrice(item))}</td><td>${item.qty}</td><td>${money(itemSubtotal(item))}</td></tr>`).join("") || `<tr><td colspan="4">訂單已沒有品項。</td></tr>`}</tbody>
            </table>
            <div class="receipt-total-row"><span>總金額</span><strong>${money(total)}</strong></div>
          </div>
        </div>
        <div class="print-receipt" style="display:none">
          <h1 style="text-align:center;margin:0 0 10px">福緣訂單明細</h1>
          <p><strong>大名：</strong>${pendingOrder.name}</p>
          <p><strong>開單時間：</strong>${pendingOrder.createdAt}</p>
          ${pendingOrder.note?`<p><strong>備註：</strong>${pendingOrder.note}</p>`:""}
          <table class="print-table">
            <thead><tr><th>商品</th><th>單價</th><th>數量</th><th>總額</th></tr></thead>
            <tbody>${pendingOrder.items.map(item=>`<tr><td>${itemName(item)}</td><td>${money(itemPrice(item))}</td><td>${item.qty}</td><td>${money(itemSubtotal(item))}</td></tr>`).join("")}</tbody>
          </table>
          <div class="print-total">總金額：${money(total)}</div>
        </div>`;
    }
    function wrapCanvasText(ctx,text,x,y,maxWidth,lineHeight){
      const words=String(text).split("");
      let line="";
      const lines=[];
      words.forEach(ch=>{
        const test=line+ch;
        if(ctx.measureText(test).width>maxWidth && line){
          lines.push(line);
          line=ch;
        }else{
          line=test;
        }
      });
      lines.push(line);
      lines.forEach((part,index)=>ctx.fillText(part,x,y+index*lineHeight));
      return Math.max(1,lines.length)*lineHeight;
    }
    function drawShareCanvas(){
      const rows=pendingOrder.items.map(item=>({
        name:itemName(item),
        price:money(itemPrice(item)),
        qty:String(item.qty),
        subtotal:money(itemSubtotal(item))
      }));
      const total=pendingOrder.items.reduce((sum,i)=>sum+itemSubtotal(i),0);
      const width=1000;
      const padding=40;
      const nameWidth=430;
      const lineHeight=30;
      const rowHeights=rows.map(row=>{
        const probe=document.createElement("canvas").getContext("2d");
        probe.font='26px "Microsoft JhengHei", sans-serif';
        const textWidth=probe.measureText(row.name).width;
        return Math.max(50,Math.ceil(textWidth/nameWidth)*lineHeight+18);
      });
      const height=230+rowHeights.reduce((a,b)=>a+b,0)+90;
      const canvas=document.createElement("canvas");
      canvas.width=width;
      canvas.height=height;
      const ctx=canvas.getContext("2d");
      ctx.fillStyle="#ffffff";
      ctx.fillRect(0,0,width,height);
      ctx.fillStyle="#111111";
      ctx.textBaseline="top";
      ctx.font='bold 42px "Microsoft JhengHei", sans-serif';
      ctx.textAlign="center";
      ctx.fillText("福緣訂單明細",width/2,28);
      ctx.textAlign="left";
      ctx.font='26px "Microsoft JhengHei", sans-serif';
      ctx.fillText(`大名：${pendingOrder.name}`,padding,94);
      ctx.fillText(`開單時間：${pendingOrder.createdAt}`,padding,132);
      if(pendingOrder.note) ctx.fillText(`備註：${pendingOrder.note}`,padding,170);
      const tableTop=pendingOrder.note?214:180;
      const cols=[padding,padding+500,padding+660,padding+780,width-padding];
      ctx.strokeStyle="#333333";
      ctx.lineWidth=2;
      ctx.font='bold 26px "Microsoft JhengHei", sans-serif';
      ctx.fillStyle="#eeeeee";
      ctx.fillRect(padding,tableTop,width-padding*2,48);
      ctx.fillStyle="#111111";
      ctx.fillText("商品",cols[0]+12,tableTop+10);
      ctx.textAlign="right";
      ctx.fillText("單價",cols[2]-12,tableTop+10);
      ctx.fillText("數量",cols[3]-12,tableTop+10);
      ctx.fillText("總額",cols[4]-12,tableTop+10);
      ctx.textAlign="left";
      let y=tableTop+48;
      ctx.font='26px "Microsoft JhengHei", sans-serif';
      rows.forEach((row,index)=>{
        const h=rowHeights[index];
        ctx.strokeRect(padding,y,width-padding*2,h);
        [cols[1],cols[2],cols[3]].forEach(x=>{ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x,y+h);ctx.stroke();});
        wrapCanvasText(ctx,row.name,cols[0]+12,y+10,nameWidth,lineHeight);
        ctx.textAlign="right";
        ctx.fillText(row.price,cols[2]-12,y+10);
        ctx.fillText(row.qty,cols[3]-12,y+10);
        ctx.fillText(row.subtotal,cols[4]-12,y+10);
        ctx.textAlign="left";
        y+=h;
      });
      ctx.font='bold 32px "Microsoft JhengHei", sans-serif';
      ctx.textAlign="right";
      ctx.fillStyle="#fff7ed";
      ctx.fillRect(padding,y+18,width-padding*2,64);
      ctx.strokeStyle="#f59e0b";
      ctx.strokeRect(padding,y+18,width-padding*2,64);
      ctx.fillStyle="#9a3412";
      ctx.fillText(`總金額：${money(total)}`,width-padding-18,y+34);
      return canvas;
    }
    async function shareReceiptImage(){
      if(!pendingOrder || !pendingOrder.items.length){
        alert("目前沒有可分享的訂單明細。");
        return;
      }
      try{
        const canvas=drawShareCanvas();
        const blob=await new Promise(resolve=>canvas.toBlob(resolve,"image/png"));
        const filename=`福緣訂單明細_${pendingOrder.name}_${Date.now()}.png`;
        const file=new File([blob],filename,{type:"image/png"});
        if(navigator.canShare && navigator.canShare({files:[file]})){
          await navigator.share({files:[file],title:"福緣訂單明細",text:`${pendingOrder.name} 訂單明細`});
        }else{
          const link=document.createElement("a");
          link.download=filename;
          link.href=URL.createObjectURL(blob);
          link.click();
          URL.revokeObjectURL(link.href);
          alert("此瀏覽器無法直接分享圖片，已改為下載明細圖片。");
        }
      }catch(error){
        alert("圖片分享未完成，可以留在此頁繼續送出訂單。");
      }
    }
    function syncPendingToPage(){
      standardCart={};
      PRODUCTS.forEach(p=>{ const input=document.getElementById("qty-"+p.id); if(input) input.value=0; });
      customCart=[];
      pendingOrder.items.forEach(item=>{
        if(item.custom) customCart.push({...item});
        else { standardCart[item.id]=item.qty; const input=document.getElementById("qty-"+item.id); if(input) input.value=item.qty; }
      });
      renderCustomList();
      updateTotal();
    }
    function clearCart(){
      document.getElementById("customerName").value="";
      document.getElementById("customerNote").value="";
      standardCart={};
      document.querySelectorAll("[data-qty]").forEach(i=>i.value=0);
      customCart=[];
      renderCustomList();
      updateTotal();
    }

    function renderAdmin(){
      const gross=state.orders.reduce((s,o)=>s+orderTotal(o),0);
      const returns=state.orders.reduce((s,o)=>s+returnedTotal(o),0);
      const pending=state.orders.filter(o=>o.status==="new"||o.status==="picking").length;
      const shipped=state.orders.filter(o=>o.status==="shipped"||o.status==="returned").length;
      const now=new Date();
      const weekStart=new Date(now); weekStart.setDate(now.getDate()-now.getDay()); weekStart.setHours(0,0,0,0);
      const monthStart=new Date(now.getFullYear(),now.getMonth(),1);
      const weekOrders=state.orders.filter(o=>orderDate(o)>=weekStart);
      const monthOrders=state.orders.filter(o=>orderDate(o)>=monthStart);
      const sumNet=orders=>orders.reduce((s,o)=>s+orderTotal(o)-returnedTotal(o),0);
      const detail=orders=>orders.map(o=>`<div class="line"><span>${dateKey(orderDate(o))}｜${o.id}<br><small>${statusText(o.status)} · 送單 ${o.createdAt||"-"}${o.shippedAt?` · 出貨 ${o.shippedAt}`:""}${o.returnedAt?` · 退貨 ${o.returnedAt}`:""}${o.returnClosedAt?` · 退貨結案 ${o.returnClosedAt}`:""}</small></span><strong>${money(orderTotal(o)-returnedTotal(o))}</strong></div>`).join("")||`<div class="empty">此區間尚無訂單。</div>`;
      document.getElementById("overview").innerHTML=`<div class="metrics"><div class="metric"><span>訂單數</span><strong>${state.orders.length}</strong></div><div class="metric"><span>待出貨</span><strong>${pending}</strong></div><div class="metric"><span>已出貨</span><strong>${shipped}</strong></div><div class="metric"><span>淨營業額</span><strong>${money(gross-returns)}</strong></div><div class="metric"><span>本週營業額</span><strong>${money(sumNet(weekOrders))}</strong></div><div class="metric"><span>本月營業額</span><strong>${money(sumNet(monthOrders))}</strong></div><div class="metric"><span>本週訂單</span><strong>${weekOrders.length}</strong></div><div class="metric"><span>本月訂單</span><strong>${monthOrders.length}</strong></div></div><h3>本週明細</h3><div class="receipt-list">${detail(weekOrders)}</div><h3>本月明細</h3><div class="receipt-list">${detail(monthOrders)}</div><h3>全部訂單</h3>${state.orders.map(orderCard).join("")||`<div class="empty">目前尚無訂單。</div>`}`;
      renderDailySummary(); renderInventory();
    }
    function orderCard(order){
      return `<div class="order-card"><div class="order-title"><span>${order.id}</span><span class="badge ${order.status}">${statusText(order.status)}</span></div><div class="meta">送單 ${order.createdAt || "-"}${order.shippedAt?` · 出貨 ${order.shippedAt}`:""}${order.returnedAt?` · 退貨 ${order.returnedAt}`:""}</div><div class="receipt-list">${order.items.map(i=>`<div class="line"><span>${itemName(i)} · 單價 ${money(itemPrice(i))} × ${i.qty}</span><strong>${money(itemSubtotal(i))}</strong></div>`).join("")}</div><div><strong>總計：</strong>${money(orderTotal(order)-returnedTotal(order))}${order.note?` ｜備註：${order.note}`:""}</div><div class="actions"><button class="danger" data-delete-order="${order.id}">刪除這筆明細</button></div></div>`;
    }
    function renderShipping(){
      const orders=state.orders.filter(o=>o.status==="new"||o.status==="picking");
      document.getElementById("shipPage").innerHTML=`<section class="category"><div class="category-title"><span>出貨劃記</span><span class="category-count">${orders.length} 張</span></div><div style="padding:10px">${orders.map(o=>`<div class="order-card"><div class="order-title"><span>${o.id}</span><span class="badge">${statusText(o.status)}</span></div><div class="meta">送單 ${o.createdAt || "-"}</div><div class="pick-list">${o.items.map(i=>`<label class="check"><input type="checkbox" data-pick="${o.id}" data-product="${i.id}" ${i.picked?"checked":""}><span>${itemName(i)} · 單價 ${money(itemPrice(i))}</span><strong>× ${i.qty}</strong></label>`).join("")}</div><div class="actions"><button class="primary" data-ship="${o.id}">完成出貨</button></div></div>`).join("")||`<div class="empty">沒有待出貨訂單。</div>`}</div></section>`;
    }
    function returnedQty(order,item){
      return (order.returns||[]).filter(r=>r.id===item.id && !!r.custom===!!item.custom && r.name===item.name).reduce((s,r)=>s+r.qty,0);
    }
    function renderReturns(){
      const orders=state.orders.filter(o=>(o.status==="shipped"||o.status==="returned") && !o.returnClosedAt);
      document.getElementById("returnPage").innerHTML=`<section class="category"><div class="category-title"><span>退貨處理</span><span class="category-count">${orders.length} 張</span></div><div style="padding:10px">${orders.map(o=>{
        const available=o.items.map((i,idx)=>({...i,idx,available:i.qty-returnedQty(o,i)})).filter(i=>i.available>0);
        return `<div class="order-card"><div class="order-title"><span>${o.id}</span><span class="badge ${o.status}">${o.status==="returned"?"已有退貨紀錄":"可退貨"}</span></div><div class="meta">${o.returnedAt?`上次退貨 ${o.returnedAt}`:`出貨 ${o.shippedAt || "-"}`}</div>${available.length?`<div class="return-grid">${available.map(i=>`<label class="return-line"><input type="checkbox" data-return-check="${o.id}" data-index="${i.idx}"><span>${itemName(i)} · 單價 ${money(itemPrice(i))}<br><small>可退 ${i.available}</small></span><input type="number" min="1" max="${i.available}" value="${i.available}" data-return-qty="${o.id}" data-index="${i.idx}"></label>`).join("")}</div><div class="actions"><button class="danger" data-complete-return="${o.id}">完成退貨並回補庫存</button><button class="secondary" data-no-return="${o.id}">不退貨，移除這張</button></div>`:`<div class="empty">此訂單所有品項都已處理退貨。</div><div class="actions"><button class="secondary" data-no-return="${o.id}">退貨完成，移除這張</button></div>`}</div>`;
      }).join("")||`<div class="empty">尚無可退貨訂單。</div>`}</div></section>`;
    }
    function renderInventory(){
      document.getElementById("inventory").innerHTML=PRODUCTS.map(p=>`<div class="inventory-row"><div><strong>${p.name}</strong><div class="meta">${productType(p)} · ${p.category} · 單價 ${money(p.price)}</div></div><div><span class="meta">庫存</span><strong>${state.stock[p.id]===null?"未控管":state.stock[p.id]}</strong></div><div><span class="meta">實銷</span><strong>${soldQty(p.id)}</strong></div><div><span class="meta">銷售額</span><strong>${money(soldQty(p.id)*p.price)}</strong></div><div class="stock-controls"><button data-stock-dec="${p.id}">−</button><input type="number" min="0" value="${state.stock[p.id]===null?0:state.stock[p.id]}" data-stock-input="${p.id}"><button data-stock-inc="${p.id}">＋</button></div></div>`).join("");
    }
    function renderDailySummary(){
      const byDate=new Map();
      state.orders.forEach(order=>{
        const key=dateKey(orderDate(order));
        if(!byDate.has(key)) byDate.set(key,new Map());
        const bucket=byDate.get(key);
        order.items.forEach(item=>{
          const keyItem=item.custom?`custom:${item.name}:${item.price}`:item.id;
          const existing=bucket.get(keyItem)||{name:itemName(item),type:item.custom?"客製化品項":productType(product(item.id)),price:itemPrice(item),qty:0,total:0};
          existing.qty+=item.qty;
          existing.total+=itemSubtotal(item);
          bucket.set(keyItem,existing);
        });
      });
      const dates=[...byDate.keys()].sort().reverse();
      document.getElementById("dailySummary").innerHTML=dates.map(day=>{
        const rows=[...byDate.get(day).values()].sort((a,b)=>a.type.localeCompare(b.type,"zh-Hant")||a.name.localeCompare(b.name,"zh-Hant"));
        const dayTotal=rows.reduce((sum,row)=>sum+row.total,0);
        return `<section class="category"><div class="category-title"><span>${day} 品項合計</span><span class="category-count">${rows.length} 項 · ${money(dayTotal)}</span></div><div class="table-wrap"><table class="receipt-table"><thead><tr><th>類型</th><th>品項</th><th>單價</th><th>合計數量</th><th>金額</th></tr></thead><tbody>${rows.map(row=>`<tr><td>${row.type}</td><td>${row.name}</td><td>${money(row.price)}</td><td>${row.qty}</td><td>${money(row.total)}</td></tr>`).join("")}</tbody></table></div></section>`;
      }).join("")||`<div class="empty">目前尚無訂單可統計。</div>`;
    }

    document.addEventListener("click", e=>{
      const minus=e.target.closest("[data-minus]"); if(minus) setQty(minus.dataset.minus,Number(document.getElementById("qty-"+minus.dataset.minus).value||0)-1);
      const plus=e.target.closest("[data-plus]"); if(plus) setQty(plus.dataset.plus,Number(document.getElementById("qty-"+plus.dataset.plus).value||0)+1);
      const close=e.target.closest("[data-close]"); if(close) closeModal(close.dataset.close);
      const customRemove=e.target.closest("[data-custom-remove]"); if(customRemove){ customCart=customCart.filter(i=>i.id!==customRemove.dataset.customRemove); renderCustomList(); }
      const customDec=e.target.closest("[data-custom-dec]"); if(customDec){ const i=customCart.find(x=>x.id===customDec.dataset.customDec); if(i) i.qty=Math.max(1,i.qty-1); renderCustomList(); }
      const customInc=e.target.closest("[data-custom-inc]"); if(customInc){ const i=customCart.find(x=>x.id===customInc.dataset.customInc); if(i) i.qty+=1; renderCustomList(); }
      const rDec=e.target.closest("[data-receipt-dec]"); if(rDec){ const i=pendingOrder.items[Number(rDec.dataset.receiptDec)]; i.qty=Math.max(1,i.qty-1); drawReceipt(); syncPendingToPage(); }
      const rInc=e.target.closest("[data-receipt-inc]"); if(rInc){ const i=pendingOrder.items[Number(rInc.dataset.receiptInc)]; if(!i.custom && state.stock[i.id]!==null) i.qty=Math.min(state.stock[i.id],i.qty+1); else i.qty+=1; drawReceipt(); syncPendingToPage(); }
      const rRemove=e.target.closest("[data-receipt-remove]"); if(rRemove){ pendingOrder.items.splice(Number(rRemove.dataset.receiptRemove),1); drawReceipt(); syncPendingToPage(); }
      const tab=e.target.closest("[data-admin-tab]"); if(tab){ document.querySelectorAll(".tab").forEach(b=>b.classList.toggle("active",b===tab)); document.querySelectorAll(".admin-view").forEach(v=>v.classList.toggle("active",v.id===tab.dataset.adminTab)); }
      const mainTab=e.target.closest("[data-main-view]"); if(mainTab) setMainView(mainTab.dataset.mainView);
      const ship=e.target.closest("[data-ship]"); if(ship){ const o=state.orders.find(x=>x.id===ship.dataset.ship); if(!o.items.every(i=>i.picked)){ alert("請先把所有品項都劃記完成。"); return; } o.status="shipped"; o.shippedAt=nowText(); o.items.forEach(i=>{ if(!i.custom && state.stock[i.id]!==null) state.stock[i.id]=Math.max(0,state.stock[i.id]-i.qty); }); saveState(); renderAdmin(); renderProducts(); renderShipping(); renderReturns(); alert(`${o.id} 已完成出貨`); }
      const completeReturn=e.target.closest("[data-complete-return]"); if(completeReturn){ const o=state.orders.find(x=>x.id===completeReturn.dataset.completeReturn); const checks=[...document.querySelectorAll(`[data-return-check="${o.id}"]:checked`)]; if(!checks.length){ alert("請至少勾選一個退貨品項。"); return; } const returned=[]; checks.forEach(ch=>{ const idx=Number(ch.dataset.index); const item=o.items[idx]; const qtyInput=document.querySelector(`[data-return-qty="${o.id}"][data-index="${idx}"]`); const max=item.qty-returnedQty(o,item); const qty=Math.max(1,Math.min(Number(qtyInput.value||1),max)); returned.push({...item,qty}); if(!item.custom && state.stock[item.id]!==null) state.stock[item.id]+=qty; }); o.returns=o.returns||[]; o.returns.push(...returned); o.status="returned"; o.returnedAt=nowText(); const hasRemaining=o.items.some(item=>item.qty-returnedQty(o,item)>0); if(!hasRemaining) o.returnClosedAt=nowText(); saveState(); renderAdmin(); renderProducts(); renderReturns(); alert(`${o.id} 已完成退貨：${returned.map(i=>itemName(i)+" × "+i.qty).join("、")}，庫存已回補。`); }
      const noReturn=e.target.closest("[data-no-return]"); if(noReturn){ const o=state.orders.find(x=>x.id===noReturn.dataset.noReturn); o.returnClosedAt=nowText(); o.returnDecision="不退貨"; saveState(); renderAdmin(); renderReturns(); alert(`${o.id} 已從退貨清單移除。`); }
      const deleteOrder=e.target.closest("[data-delete-order]"); if(deleteOrder){ const index=state.orders.findIndex(x=>x.id===deleteOrder.dataset.deleteOrder); if(index<0) return; const o=state.orders[index]; if(!confirm(`確定刪除 ${o.id}？這筆明細會從後台移除。`)) return; if(o.status==="shipped"||o.status==="returned"){ o.items.forEach(i=>{ if(!i.custom && state.stock[i.id]!==null) state.stock[i.id]+=i.qty; }); (o.returns||[]).forEach(i=>{ if(!i.custom && state.stock[i.id]!==null) state.stock[i.id]=Math.max(0,state.stock[i.id]-i.qty); }); } state.orders.splice(index,1); saveState(); renderAdmin(); renderShipping(); renderReturns(); renderProducts(); alert(`${o.id} 已刪除。`); }
      const stockDec=e.target.closest("[data-stock-dec]"); if(stockDec){ if(state.stock[stockDec.dataset.stockDec]===null) state.stock[stockDec.dataset.stockDec]=0; state.stock[stockDec.dataset.stockDec]=Math.max(0,state.stock[stockDec.dataset.stockDec]-1); saveState(); renderAdmin(); renderProducts(); }
      const stockInc=e.target.closest("[data-stock-inc]"); if(stockInc){ if(state.stock[stockInc.dataset.stockInc]===null) state.stock[stockInc.dataset.stockInc]=0; state.stock[stockInc.dataset.stockInc]+=1; saveState(); renderAdmin(); renderProducts(); }
    });

    document.addEventListener("input", e=>{
      if(e.target.matches("[data-qty]")) setQty(e.target.dataset.qty,e.target.value);
      if(e.target.id==="search") renderProducts();
      if(e.target.matches("[data-stock-input]")){ state.stock[e.target.dataset.stockInput]=Math.max(0,Number(e.target.value||0)); saveState(); renderAdmin(); renderProducts(); }
    });
    document.addEventListener("change", e=>{
      const pick=e.target.closest("[data-pick]");
      if(pick){ const o=state.orders.find(x=>x.id===pick.dataset.pick); const i=o.items.find(x=>x.id===pick.dataset.product); i.picked=pick.checked; o.status=o.items.some(x=>x.picked)?"picking":"new"; saveState(); renderAdmin(); renderShipping(); }
    });
    document.getElementById("categoryFilter").addEventListener("change",renderProducts);
    document.getElementById("addCustom").addEventListener("click",()=>{
      const name=document.getElementById("customName").value.trim();
      const price=Number(document.getElementById("customPrice").value||0);
      const qty=Math.max(1,Number(document.getElementById("customQty").value||1));
      if(!name){ alert("請輸入客製化品名。"); return; }
      customCart.push({id:"custom-"+Date.now(),custom:true,name,price,qty});
      document.getElementById("customName").value=""; document.getElementById("customPrice").value=""; document.getElementById("customQty").value=1;
      renderCustomList();
    });
    document.getElementById("openAdmin").addEventListener("click",()=>openModal("adminLogin"));
    document.getElementById("loginAdmin").addEventListener("click",()=>{ if(document.getElementById("adminPassword").value!==PASSWORD){ alert("密碼錯誤"); return; } document.getElementById("adminPassword").value=""; closeModal("adminLogin"); renderAdmin(); openModal("adminPanel"); });
    document.getElementById("checkout").addEventListener("click",()=>{ if(!document.getElementById("customerName").value.trim()){ alert("請先輸入大名。"); return; } if(!cartItems().length){ alert("請至少選擇一個品項。"); return; } renderReceipt(); openModal("receiptModal"); });
    document.getElementById("printReceipt").addEventListener("click",()=>{ window.print(); });
    document.getElementById("shareReceiptImage").addEventListener("click",shareReceiptImage);
    document.getElementById("saveOrder").addEventListener("click",()=>{
      if(!pendingOrder.items.length){ alert("訂單沒有品項，請返回修改。"); return; }
      const order={ id:makeOrderId(pendingOrder.name), name:pendingOrder.name, note:pendingOrder.note, items:pendingOrder.items.map(i=>({...i,picked:false})), status:"new", returns:[], createdAt:pendingOrder.createdAt || nowText(), createdAtISO:pendingOrder.createdAtISO || new Date().toISOString() };
      state.orders.unshift(order); saveState(); clearCart(); closeModal("receiptModal"); alert(`${order.id} 已送出。`);
    });
    initFilters(); renderProducts(); renderCustomList();
  </script>
</body>
</html>'''

final_html = html.replace("__PRODUCTS__", products_json)
Path("outputs/index.html").write_text(final_html, encoding="utf-8")
Path("index.html").write_text(final_html, encoding="utf-8")
print(f"Wrote index.html and outputs/index.html with {len(products)} products")
