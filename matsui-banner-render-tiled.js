const { chromium } = require('playwright-core');
const path=require('path'); const fs=require('fs');
const SRC=process.argv[2], OUTDIR=path.resolve(__dirname,process.argv[3]);
const SCALE=parseFloat(process.argv[4]||'3');
const transparent=process.argv[5]==='transparent';
const CW=6100, CH=3100, TILE=3050;
(async()=>{
  const FW=Math.round(CW*SCALE), FH=Math.round(CH*SCALE);
  if(!fs.existsSync(OUTDIR)) fs.mkdirSync(OUTDIR,{recursive:true});
  for(const f of fs.readdirSync(OUTDIR)) fs.unlinkSync(path.join(OUTDIR,f));
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p=await b.newPage({viewport:{width:TILE,height:TILE},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve(__dirname,SRC),{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate((tr)=>{
    const g=tr?'transparent':'#07090D';
    document.documentElement.style.cssText=`margin:0;padding:0;overflow:hidden;background:${g};`;
    document.body.style.cssText=`margin:0;padding:0;overflow:hidden;background:${g};display:block;`;
    const el=document.querySelector('.banner');
    el.style.position='absolute'; el.style.top='0'; el.style.left='0';
    el.style.transformOrigin='top left';
  }, transparent);
  const cols=Math.ceil(FW/TILE), rows=Math.ceil(FH/TILE);
  for(let r=0;r<rows;r++) for(let c=0;c<cols;c++){
    const x=c*TILE, y=r*TILE;
    await p.evaluate(({x,y,s})=>{
      document.querySelector('.banner').style.transform=`translate(${-x}px, ${-y}px) scale(${s})`;
    },{x,y,s:SCALE});
    await p.waitForTimeout(160);
    await p.screenshot({path:path.join(OUTDIR,`t_${r}_${c}.png`), omitBackground:transparent, timeout:180000});
  }
  await b.close();
  console.log(JSON.stringify({FW,FH,cols,rows,TILE}));
})();
