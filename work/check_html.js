const fs = require("fs");

const htmlPath = process.argv[2] || "outputs/index.html";
const html = fs.readFileSync(htmlPath, "utf8");
const script = html.match(/<script type="module">([\s\S]*)<\/script>/)[1];
const {spawnSync}=require('node:child_process');
const check=spawnSync(process.execPath,['--check','--input-type=module'],{input:script,encoding:'utf8'});
if(check.status!==0)throw Error(check.stderr);

if(!script.includes("FuyuanCloud.loadProducts('order')"))throw Error('Missing shared catalog connection');
console.log("Module JS syntax OK; catalog loads from shared API");
