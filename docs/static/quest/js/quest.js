const sfxToggle = document.getElementById('sfxToggle');
const radio = document.getElementById('snd-radio');
const typeTick = document.getElementById('snd-type');
let sfxOn = false;

function setSfx(on){
  sfxOn = on;
  if (sfxToggle){
    sfxToggle.textContent = on ? 'í´Š SFX: On' : 'í´‡ SFX: Off';
    sfxToggle.setAttribute('aria-pressed', String(on));
  }
  if (!radio) return;
  if (on){ radio.play().catch(()=>{}); }
  else { radio.pause(); radio.currentTime = 0; }
}

sfxToggle?.addEventListener('click', ()=> setSfx(!sfxOn));
document.addEventListener('visibilitychange', ()=> {
  if (document.hidden && !radio.paused){ radio.pause(); }
  else if (!document.hidden && sfxOn){ radio.play().catch(()=>{}); }
});
window.addEventListener('load', ()=>{
  setTimeout(()=> { if (sfxOn) typeTick?.play().catch(()=>{}); }, 3200);
});
