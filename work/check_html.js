const fs = require("fs");

const htmlPath = process.argv[2] || "outputs/index.html";
const html = fs.readFileSync(htmlPath, "utf8");
const script = html.match(/<script type="module">([\s\S]*)<\/script>/)[1];
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
new AsyncFunction(script);

if(!script.includes("FuyuanCloud.loadProducts('order')"))throw Error('Missing shared catalog connection');
console.log("Module JS syntax OK; catalog loads from shared API");
