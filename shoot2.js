const { chromium } = require("playwright");
const OUT = "/home/user/grosjean/shots";
(async () => {
  const b = await chromium.launch({ executablePath:"/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args:["--no-sandbox"] });
  const p = await b.newPage({ viewport:{width:1440,height:900}, deviceScaleFactor:1.25 });
  await p.goto("http://localhost:3000/", { waitUntil:"networkidle", timeout:60000 });
  for (const [sel,name] of [["#produits","produits"],["#services","services"],["#depots","depots"],["#faq","faq"]]) {
    await p.evaluate((s)=>document.querySelector(s)?.scrollIntoView({behavior:"instant",block:"start"}), sel);
    await p.waitForTimeout(1400);
    await p.screenshot({ path:`${OUT}/${name}.png` });
  }
  console.log("ok");
  await b.close();
})().catch(e=>{console.error(e.message);process.exit(1);});
