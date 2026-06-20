const fs = require("fs");

const htmlPath = process.argv[2] || "outputs/index.html";
const html = fs.readFileSync(htmlPath, "utf8");
const script = html.match(/<script>([\s\S]*)<\/script>/)[1];
new Function(script);

const productCount = (html.match(/"id": "p/g) || []).length;
console.log("JS syntax OK");
console.log(`${productCount} products embedded`);
