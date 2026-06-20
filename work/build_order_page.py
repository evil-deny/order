from pathlib import Path
import json
import re

SOURCE = Path(r"C:\Users\煞氣\Desktop\煞氣\index.html")
OUTPUT = Path("outputs/index.html")


def extract_products():
    text = SOURCE.read_text(encoding="utf-8")
    pattern = re.compile(
        r'\{\s*category:\s*"(?P<cat>.*?)",\s*'
        r'name:\s*"(?P<name>.*?)",\s*'
        r'price:\s*(?P<price>\d+),\s*'
        r'stock:\s*(?P<stock>null|\d+),\s*'
        r'image:\s*"(?P<img>.*?)"\s*\}',
        re.S,
    )
    products = []
    for index, match in enumerate(pattern.finditer(text)):
        item = match.groupdict()
        products.append(
            {
                "id": f"p{index + 1}",
                "category": item["cat"].strip(),
                "name": item["name"].strip(),
                "price": int(item["price"]),
                "stock": None if item["stock"] == "null" else int(item["stock"]),
                "image": item["img"].strip(),
            }
        )
    return products


products_json = json.dumps(extract_products(), ensure_ascii=False)

html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>團購訂單系統</title>
  <style>
    :root {{
      --bg: #f5f7fa;
      --card: #ffffff;
      --ink: #1f2937;
      --muted: #64748b;
      --line: #d8e0ea;
      --main: #0f766e;
      --main-dark: #115e59;
      --blue: #2563eb;
      --red: #dc2626;
      --amber: #b45309;
      --shadow: 0 10px 24px rgba(15, 23, 42, .08);
      font-family: "Microsoft JhengHei", "Noto Sans TC", system-ui, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      background: var(--bg);
      letter-spacing: 0;
      font-size: 16px;
    }}
    button, input, select, textarea {{ font: inherit; }}
    button {{
      border: 0;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 800;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 20;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 14px clamp(12px, 3vw, 28px);
      background: #fff;
      border-bottom: 1px solid var(--line);
      box-shadow: 0 2px 10px rgba(15, 23, 42, .05);
    }}
    .brand strong {{ display: block; font-size: 22px; line-height: 1.1; }}
    .brand span {{ display: block; color: var(--muted); font-size: 13px; margin-top: 3px; }}
    .admin-open {{
      min-height: 40px;
      padding: 0 14px;
      background: #e8eef5;
      color: #243244;
      white-space: nowrap;
    }}
    .wrap {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 14px 12px 112px;
    }}
    .customer-box {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 10px;
      padding: 12px;
      margin-bottom: 12px;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 10px;
      box-shadow: var(--shadow);
    }}
    label {{ display: grid; gap: 6px; color: var(--muted); font-size: 14px; font-weight: 800; }}
    input, textarea, select {{
      width: 100%;
      min-height: 46px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--ink);
      background: #fff;
      outline: none;
    }}
    input:focus, textarea:focus, select:focus {{ border-color: var(--main); box-shadow: 0 0 0 3px rgba(15, 118, 110, .12); }}
    .search-row {{
      position: sticky;
      top: 72px;
      z-index: 15;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 150px;
      gap: 10px;
      padding: 10px 0;
      background: var(--bg);
    }}
    .category {{
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: 10px;
      overflow: hidden;
      background: var(--card);
      box-shadow: var(--shadow);
    }}
    .category-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px;
      background: #eef5f5;
      border-bottom: 1px solid var(--line);
      font-size: 19px;
      font-weight: 900;
    }}
    .category-count {{ color: var(--muted); font-size: 13px; font-weight: 700; }}
    .items {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      padding: 10px;
    }}
    .item {{
      display: grid;
      grid-template-columns: 82px minmax(0, 1fr);
      gap: 10px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 9px;
      background: #fff;
    }}
    .item img {{
      width: 82px;
      height: 82px;
      object-fit: cover;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #f1f5f9;
    }}
    .item h3 {{
      margin: 0;
      font-size: 17px;
      line-height: 1.35;
      word-break: break-word;
    }}
    .meta {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      margin: 7px 0 10px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
    }}
    .price {{ color: var(--red); font-size: 17px; }}
    .stock {{ color: var(--amber); background: #fff7ed; padding: 2px 7px; border-radius: 99px; }}
    .qty {{
      display: grid;
      grid-template-columns: 42px minmax(48px, 1fr) 42px;
      gap: 7px;
      align-items: center;
    }}
    .qty button {{
      width: 42px;
      height: 42px;
      background: #e2e8f0;
      color: #243244;
      font-size: 22px;
    }}
    .qty input {{
      min-height: 42px;
      text-align: center;
      padding: 4px;
      font-size: 20px;
      font-weight: 900;
    }}
    .bottom-bar {{
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 25;
      display: flex;
      justify-content: center;
      padding: 10px 12px;
      background: rgba(255,255,255,.96);
      border-top: 1px solid var(--line);
      box-shadow: 0 -8px 24px rgba(15, 23, 42, .08);
    }}
    .bottom-inner {{
      width: min(1120px, 100%);
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      align-items: center;
    }}
    .total {{
      font-size: 15px;
      color: var(--muted);
      font-weight: 800;
    }}
    .total strong {{
      display: block;
      color: var(--red);
      font-size: 28px;
      line-height: 1.05;
    }}
    .checkout {{
      min-height: 54px;
      padding: 0 22px;
      background: var(--main);
      color: #fff;
      font-size: 18px;
    }}
    .modal {{
      display: none;
      position: fixed;
      inset: 0;
      z-index: 50;
      background: rgba(15, 23, 42, .55);
      padding: 12px;
      align-items: center;
      justify-content: center;
    }}
    .modal.show {{ display: flex; }}
    .modal-card {{
      width: min(980px, 100%);
      max-height: 92vh;
      overflow: auto;
      background: #fff;
      border-radius: 12px;
      box-shadow: 0 24px 60px rgba(15, 23, 42, .25);
    }}
    .modal-head {{
      position: sticky;
      top: 0;
      z-index: 2;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      padding: 14px 16px;
      background: #fff;
      border-bottom: 1px solid var(--line);
    }}
    .modal-head h2 {{ margin: 0; font-size: 21px; }}
    .close {{ width: 40px; height: 40px; background: #e2e8f0; }}
    .modal-body {{ padding: 16px; }}
    .receipt-list, .pick-list {{ display: grid; gap: 8px; margin: 12px 0; }}
    .line {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 10px;
      padding: 10px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
    }}
    .actions {{ display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }}
    .primary {{ min-height: 44px; padding: 0 14px; color: #fff; background: var(--main); }}
    .secondary {{ min-height: 44px; padding: 0 14px; background: #e2e8f0; color: #243244; }}
    .danger {{ min-height: 44px; padding: 0 14px; color: #fff; background: var(--red); }}
    .admin-tabs {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 8px;
      margin-bottom: 14px;
    }}
    .tab {{
      min-height: 44px;
      background: #e2e8f0;
      color: #243244;
    }}
    .tab.active {{ background: var(--main); color: #fff; }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 14px;
    }}
    .metric {{
      padding: 14px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #f8fafc;
    }}
    .metric span {{ color: var(--muted); font-size: 13px; font-weight: 800; }}
    .metric strong {{ display: block; margin-top: 7px; font-size: 25px; }}
    .admin-view {{ display: none; }}
    .admin-view.active {{ display: block; }}
    .order-card, .inventory-row {{
      display: grid;
      gap: 10px;
      padding: 12px;
      margin-bottom: 10px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fff;
    }}
    .order-title {{
      display: flex;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      font-weight: 900;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 26px;
      padding: 2px 9px;
      border-radius: 99px;
      background: #dbeafe;
      color: #1d4ed8;
      font-size: 13px;
      font-weight: 900;
    }}
    .badge.shipped {{ background: #dcfce7; color: #166534; }}
    .badge.returned {{ background: #fee2e2; color: #991b1b; }}
    .check {{
      display: grid;
      grid-template-columns: 24px minmax(0, 1fr) auto;
      gap: 8px;
      align-items: center;
      padding: 9px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f8fafc;
    }}
    .check input {{ width: 20px; min-height: 20px; accent-color: var(--main); }}
    .inventory-row {{
      grid-template-columns: minmax(0, 1.4fr) 100px 100px 130px;
      align-items: center;
    }}
    .empty {{
      padding: 24px;
      color: var(--muted);
      text-align: center;
      border: 1px dashed var(--line);
      border-radius: 10px;
      background: #f8fafc;
    }}
    @media (max-width: 760px) {{
      .topbar {{ padding: 12px; }}
      .brand strong {{ font-size: 19px; }}
      .wrap {{ padding-bottom: 122px; }}
      .customer-box, .search-row, .items, .bottom-inner, .metrics, .inventory-row {{
        grid-template-columns: 1fr;
      }}
      .search-row {{ top: 65px; }}
      .item {{
        grid-template-columns: 76px minmax(0, 1fr);
        padding: 9px;
      }}
      .item img {{ width: 76px; height: 76px; }}
      .item h3 {{ font-size: 16px; }}
      .qty {{ grid-template-columns: 40px minmax(46px, 1fr) 40px; }}
      .qty button {{ width: 40px; height: 40px; }}
      .checkout {{ width: 100%; }}
      .admin-tabs {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .modal-body {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <strong>團購訂單系統</strong>
      <span>輸入大名，選品項，確認後送出</span>
    </div>
    <button class="admin-open" id="openAdmin">後台</button>
  </header>

  <main class="wrap">
    <section class="customer-box">
      <label>大名
        <input id="customerName" autocomplete="name" placeholder="請輸入大名">
      </label>
      <label>備註
        <input id="customerNote" placeholder="例：不要辣、分開裝、晚點取">
      </label>
    </section>

    <section class="search-row">
      <input id="search" type="search" placeholder="搜尋品項名稱">
      <select id="categoryFilter" aria-label="分類篩選"></select>
    </section>

    <div id="productList"></div>
  </main>

  <footer class="bottom-bar">
    <div class="bottom-inner">
      <div class="total">合計 <strong id="cartTotal">$0</strong></div>
      <button class="checkout" id="checkout">確認訂單</button>
    </div>
  </footer>

  <section class="modal" id="receiptModal" aria-hidden="true">
    <div class="modal-card">
      <div class="modal-head">
        <h2>訂單確認</h2>
        <button class="close" data-close="receiptModal">×</button>
      </div>
      <div class="modal-body">
        <div id="receiptContent"></div>
        <div class="actions">
          <button class="secondary" data-close="receiptModal">返回修改</button>
          <button class="primary" id="saveOrder">送出訂單</button>
        </div>
      </div>
    </div>
  </section>

  <section class="modal" id="adminLogin" aria-hidden="true">
    <div class="modal-card" style="max-width:420px">
      <div class="modal-head">
        <h2>後台登入</h2>
        <button class="close" data-close="adminLogin">×</button>
      </div>
      <div class="modal-body">
        <label>密碼
          <input id="adminPassword" type="password" inputmode="numeric" placeholder="預設 0000">
        </label>
        <div class="actions">
          <button class="primary" id="loginAdmin">進入後台</button>
        </div>
      </div>
    </div>
  </section>

  <section class="modal" id="adminPanel" aria-hidden="true">
    <div class="modal-card">
      <div class="modal-head">
        <h2>後台管理</h2>
        <button class="close" data-close="adminPanel">×</button>
      </div>
      <div class="modal-body">
        <div class="admin-tabs">
          <button class="tab active" data-admin-tab="overview">總覽</button>
          <button class="tab" data-admin-tab="shipping">出貨劃記</button>
          <button class="tab" data-admin-tab="returns">退貨</button>
          <button class="tab" data-admin-tab="inventory">庫存</button>
        </div>
        <div class="admin-view active" id="overview"></div>
        <div class="admin-view" id="shipping"></div>
        <div class="admin-view" id="returns"></div>
        <div class="admin-view" id="inventory"></div>
      </div>
    </div>
  </section>

  <script>
    const PRODUCTS = {products_json};
    const PASSWORD = "0000";
    const STORE_KEY = "clearOrderSystemV2";
    const PLACEHOLDER = "https://via.placeholder.com/120x120?text=No+Image";

    const state = loadState();
    let pendingOrder = null;

    function loadState() {{
      const saved = localStorage.getItem(STORE_KEY);
      if (saved) return JSON.parse(saved);
      return {{
        orders: [],
        stock: Object.fromEntries(PRODUCTS.map(p => [p.id, p.stock === null ? null : p.stock]))
      }};
    }}

    function saveState() {{
      localStorage.setItem(STORE_KEY, JSON.stringify(state));
    }}

    function money(value) {{
      return "$" + Number(value || 0).toLocaleString("zh-TW");
    }}

    function product(id) {{
      return PRODUCTS.find(p => p.id === id);
    }}

    function cartItems() {{
      return PRODUCTS.map(p => {{
        const qty = Number(document.getElementById("qty-" + p.id)?.value || 0);
        return {{ id: p.id, qty }};
      }}).filter(item => item.qty > 0);
    }}

    function orderTotal(order) {{
      return order.items.reduce((sum, item) => sum + product(item.id).price * item.qty, 0);
    }}

    function returnedTotal(order) {{
      return (order.returns || []).reduce((sum, item) => sum + product(item.id).price * item.qty, 0);
    }}

    function soldQty(productId) {{
      return state.orders.reduce((sum, order) => {{
        if (order.status !== "shipped" && order.status !== "returned") return sum;
        const sold = order.items.filter(i => i.id === productId).reduce((n, i) => n + i.qty, 0);
        const returned = (order.returns || []).filter(i => i.id === productId).reduce((n, i) => n + i.qty, 0);
        return sum + sold - returned;
      }}, 0);
    }}

    function statusText(status) {{
      return {{ new: "待出貨", picking: "揀貨中", shipped: "已出貨", returned: "有退貨" }}[status] || status;
    }}

    function openModal(id) {{
      document.getElementById(id).classList.add("show");
      document.getElementById(id).setAttribute("aria-hidden", "false");
    }}

    function closeModal(id) {{
      document.getElementById(id).classList.remove("show");
      document.getElementById(id).setAttribute("aria-hidden", "true");
    }}

    function initFilters() {{
      const categories = ["全部分類", ...new Set(PRODUCTS.map(p => p.category))];
      document.getElementById("categoryFilter").innerHTML = categories.map(c => `<option value="${{c}}">${{c}}</option>`).join("");
    }}

    function visibleProducts() {{
      const keyword = document.getElementById("search").value.trim().toLowerCase();
      const cat = document.getElementById("categoryFilter").value;
      return PRODUCTS.filter(p => {{
        const matchText = p.name.toLowerCase().includes(keyword);
        const matchCat = cat === "全部分類" || p.category === cat;
        return matchText && matchCat;
      }});
    }}

    function renderProducts() {{
      const grouped = new Map();
      visibleProducts().forEach(p => {{
        if (!grouped.has(p.category)) grouped.set(p.category, []);
        grouped.get(p.category).push(p);
      }});
      const html = [...grouped.entries()].map(([category, items]) => `
        <section class="category">
          <div class="category-title">
            <span>${{category}}</span>
            <span class="category-count">${{items.length}} 項</span>
          </div>
          <div class="items">
            ${{items.map(p => `
              <article class="item">
                <img src="${{p.image || PLACEHOLDER}}" alt="${{p.name}}" loading="lazy" onerror="this.src='${{PLACEHOLDER}}'">
                <div>
                  <h3>${{p.name}}</h3>
                  <div class="meta">
                    <span class="price">${{money(p.price)}}</span>
                    ${{state.stock[p.id] === null ? "" : `<span class="stock">庫存 ${{state.stock[p.id]}}</span>`}}
                  </div>
                  <div class="qty">
                    <button type="button" data-minus="${{p.id}}">−</button>
                    <input id="qty-${{p.id}}" type="number" min="0" value="0" inputmode="numeric" data-qty="${{p.id}}">
                    <button type="button" data-plus="${{p.id}}">＋</button>
                  </div>
                </div>
              </article>
            `).join("")}}
          </div>
        </section>
      `).join("");
      document.getElementById("productList").innerHTML = html || `<div class="empty">找不到品項。</div>`;
      updateTotal();
    }}

    function updateTotal() {{
      const total = cartItems().reduce((sum, item) => sum + product(item.id).price * item.qty, 0);
      document.getElementById("cartTotal").textContent = money(total);
    }}

    function setQty(id, qty) {{
      const input = document.getElementById("qty-" + id);
      const stock = state.stock[id];
      let next = Math.max(0, Number(qty || 0));
      if (stock !== null) next = Math.min(next, stock);
      input.value = next;
      updateTotal();
    }}

    function renderReceipt() {{
      const name = document.getElementById("customerName").value.trim();
      const note = document.getElementById("customerNote").value.trim();
      const items = cartItems();
      const total = items.reduce((sum, item) => sum + product(item.id).price * item.qty, 0);
      document.getElementById("receiptContent").innerHTML = `
        <p><strong>大名：</strong>${{name}}</p>
        ${{note ? `<p><strong>備註：</strong>${{note}}</p>` : ""}}
        <div class="receipt-list">
          ${{items.map(item => `<div class="line"><span>${{product(item.id).name}} × ${{item.qty}}</span><strong>${{money(product(item.id).price * item.qty)}}</strong></div>`).join("")}}
        </div>
        <div class="line"><strong>總計</strong><strong>${{money(total)}}</strong></div>
      `;
      pendingOrder = {{ name, note, items, total }};
    }}

    function clearCart() {{
      document.getElementById("customerName").value = "";
      document.getElementById("customerNote").value = "";
      document.querySelectorAll("[data-qty]").forEach(input => input.value = 0);
      updateTotal();
    }}

    function renderAdmin() {{
      const gross = state.orders.reduce((sum, order) => sum + orderTotal(order), 0);
      const returns = state.orders.reduce((sum, order) => sum + returnedTotal(order), 0);
      const pending = state.orders.filter(o => o.status === "new" || o.status === "picking").length;
      const shipped = state.orders.filter(o => o.status === "shipped" || o.status === "returned").length;
      document.getElementById("overview").innerHTML = `
        <div class="metrics">
          <div class="metric"><span>訂單數</span><strong>${{state.orders.length}}</strong></div>
          <div class="metric"><span>待出貨</span><strong>${{pending}}</strong></div>
          <div class="metric"><span>已出貨</span><strong>${{shipped}}</strong></div>
          <div class="metric"><span>淨營業額</span><strong>${{money(gross - returns)}}</strong></div>
        </div>
        ${{state.orders.map(orderCard).join("") || `<div class="empty">目前尚無訂單。</div>`}}
      `;
      renderShipping();
      renderReturns();
      renderInventory();
    }}

    function orderCard(order) {{
      return `
        <div class="order-card">
          <div class="order-title">
            <span>${{order.id}} · ${{order.name}}</span>
            <span class="badge ${{order.status}}">${{statusText(order.status)}}</span>
          </div>
          <div class="receipt-list">
            ${{order.items.map(item => `<div class="line"><span>${{product(item.id).name}} × ${{item.qty}}</span><strong>${{money(product(item.id).price * item.qty)}}</strong></div>`).join("")}}
          </div>
          <div><strong>總計：</strong>${{money(orderTotal(order) - returnedTotal(order))}} ${{order.note ? `｜備註：${{order.note}}` : ""}}</div>
        </div>
      `;
    }}

    function renderShipping() {{
      const orders = state.orders.filter(o => o.status === "new" || o.status === "picking");
      document.getElementById("shipping").innerHTML = orders.map(order => `
        <div class="order-card">
          <div class="order-title"><span>${{order.id}} · ${{order.name}}</span><span class="badge">${{statusText(order.status)}}</span></div>
          <div class="pick-list">
            ${{order.items.map(item => `
              <label class="check">
                <input type="checkbox" data-pick="${{order.id}}" data-product="${{item.id}}" ${{item.picked ? "checked" : ""}}>
                <span>${{product(item.id).name}}</span>
                <strong>× ${{item.qty}}</strong>
              </label>
            `).join("")}}
          </div>
          <div class="actions"><button class="primary" data-ship="${{order.id}}">完成出貨</button></div>
        </div>
      `).join("") || `<div class="empty">沒有待出貨訂單。</div>`;
    }}

    function renderReturns() {{
      const orders = state.orders.filter(o => o.status === "shipped" || o.status === "returned");
      document.getElementById("returns").innerHTML = orders.map(order => `
        <div class="order-card">
          <div class="order-title"><span>${{order.id}} · ${{order.name}}</span><span class="badge ${{order.status}}">${{statusText(order.status)}}</span></div>
          <label>退貨品項
            <select data-return-product="${{order.id}}">
              ${{order.items.map(item => `<option value="${{item.id}}">${{product(item.id).name}}，最多 ${{item.qty}}</option>`).join("")}}
            </select>
          </label>
          <label>退貨數量
            <input type="number" min="1" value="1" data-return-qty="${{order.id}}">
          </label>
          <div class="actions"><button class="danger" data-return="${{order.id}}">登記退貨</button></div>
        </div>
      `).join("") || `<div class="empty">尚無可退貨訂單。</div>`;
    }}

    function renderInventory() {{
      document.getElementById("inventory").innerHTML = PRODUCTS.map(p => `
        <div class="inventory-row">
          <div><strong>${{p.name}}</strong><div class="meta">${{p.category}}</div></div>
          <div><span class="meta">庫存</span><strong>${{state.stock[p.id] === null ? "未控管" : state.stock[p.id]}}</strong></div>
          <div><span class="meta">實銷</span><strong>${{soldQty(p.id)}}</strong></div>
          <div><span class="meta">銷售額</span><strong>${{money(soldQty(p.id) * p.price)}}</strong></div>
        </div>
      `).join("");
    }}

    document.addEventListener("click", event => {{
      const minus = event.target.closest("[data-minus]");
      if (minus) setQty(minus.dataset.minus, Number(document.getElementById("qty-" + minus.dataset.minus).value || 0) - 1);
      const plus = event.target.closest("[data-plus]");
      if (plus) setQty(plus.dataset.plus, Number(document.getElementById("qty-" + plus.dataset.plus).value || 0) + 1);
      const close = event.target.closest("[data-close]");
      if (close) closeModal(close.dataset.close);
      const tab = event.target.closest("[data-admin-tab]");
      if (tab) {{
        document.querySelectorAll(".tab").forEach(btn => btn.classList.toggle("active", btn === tab));
        document.querySelectorAll(".admin-view").forEach(view => view.classList.toggle("active", view.id === tab.dataset.adminTab));
      }}
      const ship = event.target.closest("[data-ship]");
      if (ship) {{
        const order = state.orders.find(o => o.id === ship.dataset.ship);
        if (!order.items.every(i => i.picked)) {{
          alert("請先把所有品項都劃記完成。");
          return;
        }}
        order.status = "shipped";
        order.items.forEach(item => {{
          if (state.stock[item.id] !== null) state.stock[item.id] = Math.max(0, state.stock[item.id] - item.qty);
        }});
        saveState();
        renderAdmin();
        renderProducts();
      }}
      const ret = event.target.closest("[data-return]");
      if (ret) {{
        const order = state.orders.find(o => o.id === ret.dataset.return);
        const productId = document.querySelector(`[data-return-product="${{order.id}}"]`).value;
        const qty = Math.max(1, Number(document.querySelector(`[data-return-qty="${{order.id}}"]`).value || 1));
        const max = order.items.find(i => i.id === productId).qty;
        const finalQty = Math.min(qty, max);
        order.status = "returned";
        order.returns = order.returns || [];
        order.returns.push({{ id: productId, qty: finalQty }});
        if (state.stock[productId] !== null) state.stock[productId] += finalQty;
        saveState();
        renderAdmin();
        renderProducts();
      }}
    }});

    document.addEventListener("input", event => {{
      if (event.target.matches("[data-qty]")) setQty(event.target.dataset.qty, event.target.value);
      if (event.target.id === "search") renderProducts();
    }});

    document.getElementById("categoryFilter").addEventListener("change", renderProducts);
    document.getElementById("openAdmin").addEventListener("click", () => openModal("adminLogin"));
    document.getElementById("loginAdmin").addEventListener("click", () => {{
      if (document.getElementById("adminPassword").value !== PASSWORD) {{
        alert("密碼錯誤");
        return;
      }}
      document.getElementById("adminPassword").value = "";
      closeModal("adminLogin");
      renderAdmin();
      openModal("adminPanel");
    }});
    document.getElementById("checkout").addEventListener("click", () => {{
      if (!document.getElementById("customerName").value.trim()) {{
        alert("請先輸入大名。");
        return;
      }}
      if (!cartItems().length) {{
        alert("請至少選擇一個品項。");
        return;
      }}
      renderReceipt();
      openModal("receiptModal");
    }});
    document.getElementById("saveOrder").addEventListener("click", () => {{
      const order = {{
        id: "ORD-" + new Date().toISOString().slice(2, 10).replaceAll("-", "") + "-" + String(state.orders.length + 1).padStart(3, "0"),
        name: pendingOrder.name,
        note: pendingOrder.note,
        items: pendingOrder.items.map(item => ({{ ...item, picked: false }})),
        status: "new",
        returns: [],
        createdAt: new Date().toLocaleString("zh-TW", {{ hour12: false }})
      }};
      state.orders.unshift(order);
      saveState();
      clearCart();
      closeModal("receiptModal");
      alert("訂單已送出，謝謝。");
    }});
    document.addEventListener("change", event => {{
      const pick = event.target.closest("[data-pick]");
      if (!pick) return;
      const order = state.orders.find(o => o.id === pick.dataset.pick);
      const item = order.items.find(i => i.id === pick.dataset.product);
      item.picked = pick.checked;
      order.status = order.items.some(i => i.picked) ? "picking" : "new";
      saveState();
      renderAdmin();
    }});

    initFilters();
    renderProducts();
  </script>
</body>
</html>
"""

OUTPUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUTPUT} with {len(extract_products())} products")
