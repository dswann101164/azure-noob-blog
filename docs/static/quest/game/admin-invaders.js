const c = document.getElementById('cv'), x = c.getContext('2d');
const W=c.width, H=c.height;
let left=false, right=false, fire=false, frame=0, score=0, over=false;

const player = {x: W/2, y:H-50, w:40, h:12, vx:6};
const shots=[], crates=[], shields=[];
function spawnCrate(){ crates.push({x:Math.random()*(W-60)+30, y:-20, vy:1.2+Math.random()*1.2, r:18, t:'UNTAGGED'}); }
function spawnShield(){ shields.push({x:Math.random()*(W-60)+30, y:-20, vy:1+Math.random(), r:14, t:'POLICY'}); }

addEventListener('keydown',e=>{ if(e.key==='ArrowLeft')left=true; if(e.key==='ArrowRight')right=true; if(e.code==='Space')fire=true; });
addEventListener('keyup',e=>{ if(e.key==='ArrowLeft')left=false; if(e.key==='ArrowRight')right=false; if(e.code==='Space')fire=false; });

function step(){
  if(over) return draw();
  frame++;

  if(left) player.x-=player.vx;
  if(right) player.x+=player.vx;
  player.x=Math.max(30,Math.min(W-30,player.x));

  if(frame%8===0 && fire) shots.push({x:player.x, y:player.y-16, vy: -6});

  if(frame%55===0) spawnCrate();
  if(frame%180===0) spawnShield();

  shots.forEach(s=> s.y+=s.vy);
  crates.forEach(a=> a.y+=a.vy);
  shields.forEach(a=> a.y+=a.vy);

  for(let i=crates.length-1;i>=0;i--){
    for(let j=shots.length-1;j>=0;j--){
      const a=crates[i], s=shots[j];
      if((s.x-a.x)**2+(s.y-a.y)**2 < (a.r+4)**2){
        crates.splice(i,1); shots.splice(j,1); score+=25; break;
      }
    }
  }
  for(let i=shields.length-1;i>=0;i--){
    const a=shields[i];
    if((player.x-a.x)**2+(player.y-a.y)**2 < (a.r+22)**2){
      shields.splice(i,1); score+=15;
    }
  }
  crates.forEach(a=> { if(a.y>H-30) over=true; });

  draw(); requestAnimationFrame(step);
}

function draw(){
  x.clearRect(0,0,W,H);
  x.fillStyle='#131821'; x.fillRect(0,H-30,W,30);
  x.fillStyle='#f7f3e8'; x.font='18px monospace';
  x.fillText('SCORE: '+String(score).padStart(4,'0'), 18, 28);
  x.fillStyle='#8fbf7f'; x.fillRect(player.x-20,player.y-6,40,12);
  x.fillRect(player.x-2,player.y-14,4,8);
  x.fillStyle='#f0c040'; shots.forEach(s=> x.fillRect(s.x-2,s.y-6,4,8));
  crates.forEach(a=>{
    x.fillStyle='#c75f5f'; x.beginPath(); x.arc(a.x,a.y,a.r,0,Math.PI*2); x.fill();
    x.fillStyle='#111'; x.font='bold 12px monospace'; x.textAlign='center'; x.fillText('UNTAGGED', a.x, a.y+4);
  });
  shields.forEach(a=>{
    x.strokeStyle='#7fb0ff'; x.lineWidth=3; x.beginPath(); x.arc(a.x,a.y,a.r,0,Math.PI*2); x.stroke();
    x.fillStyle='#7fb0ff'; x.font='bold 12px monospace'; x.textAlign='center'; x.fillText('POLICY', a.x, a.y+4);
  });
  if(over){
    x.fillStyle='rgba(0,0,0,.6)'; x.fillRect(0,0,W,H);
    x.fillStyle='#f7f3e8'; x.textAlign='center'; x.font='bold 28px monospace';
    x.fillText('FRONTLINE BREACHED', W/2, H/2-10);
    x.font='16px monospace'; x.fillText('Press R to retry', W/2, H/2+18);
  }
}
addEventListener('keydown',e=>{ if(over && (e.key==='r' || e.key==='R')){ location.reload(); }});
draw(); requestAnimationFrame(step);
