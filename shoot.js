const { chromium } = require("playwright");
const OUT = "/home/user/grosjean/shots";
require("fs").mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch({ executablePath:"/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args:["--no-sandbox"] });
  const p = await b.newPage({ viewport:{width:1440,height:900}, deviceScaleFactor:1.25 });
  let errs=[]; p.on("pageerror",e=>errs.push(e.message));
  await p.goto("http://localhost:3000/", { waitUntil:"networkidle", timeout:60000 });
  await p.waitForTimeout(2500);
  await p.screenshot({ path:`${OUT}/hero.png` });
  // full page
  await p.screenshot({ path:`${OUT}/full.png`, fullPage:true });
  // mobile
  const m = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:2 });
  await m.goto("http://localhost:3000/", { waitUntil:"networkidle", timeout:60000 });
  await m.waitForTimeout(2000);
  await m.screenshot({ path:`${OUT}/mobile.png` });
  console.log("pageerrors:", errs.length?errs.slice(0,3):"none");
  await b.close();
})().catch(e=>{console.error(e.message);process.exit(1);});
