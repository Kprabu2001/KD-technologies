/* ============================================
   KD Technologies — Main JS
   ============================================ */

// ── NAVBAR ──────────────────────────────────
const navbar   = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
const allNavLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
  updateActiveNav();
});

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('open');
  navLinks.classList.toggle('open');
});

navLinks.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navLinks.classList.remove('open');
  });
});

function updateActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  let current = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 120) current = sec.id;
  });
  allNavLinks.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
  });
}

// ── HERO CANVAS ANIMATION ────────────────────
const canvas = document.getElementById('heroCanvas');
const ctx    = canvas.getContext('2d');
let particles = [];
let W, H;

function resize() {
  W = canvas.width  = canvas.offsetWidth;
  H = canvas.height = canvas.offsetHeight;
}
window.addEventListener('resize', resize);
resize();

class Particle {
  constructor() { this.reset(); }
  reset() {
    this.x  = Math.random() * W;
    this.y  = Math.random() * H;
    this.r  = Math.random() * 2 + 0.5;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.alpha = Math.random() * 0.6 + 0.1;
    const colors = ['124,58,237','6,182,212','244,114,182'];
    this.color = colors[Math.floor(Math.random() * colors.length)];
  }
  update() {
    this.x += this.vx;
    this.y += this.vy;
    if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
  }
  draw() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${this.color},${this.alpha})`;
    ctx.fill();
  }
}

// Glowing blobs
const blobs = [
  { x: 0.25, y: 0.3, r: 300, color: '124,58,237', alpha: 0.12, dx: 0.0003, dy: 0.0002 },
  { x: 0.75, y: 0.6, r: 250, color: '6,182,212',  alpha: 0.10, dx: -0.0002, dy: 0.0003 },
  { x: 0.5,  y: 0.8, r: 200, color: '244,114,182',alpha: 0.08,  dx: 0.0002, dy: -0.0002 },
];
let tick = 0;

// Init particles
for (let i = 0; i < 120; i++) particles.push(new Particle());

function drawConnections() {
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x;
      const dy = particles[i].y - particles[j].y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 100) {
        ctx.beginPath();
        ctx.moveTo(particles[i].x, particles[i].y);
        ctx.lineTo(particles[j].x, particles[j].y);
        ctx.strokeStyle = `rgba(124,58,237,${0.06 * (1 - dist / 100)})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }
}

function animate() {
  ctx.clearRect(0, 0, W, H);
  tick++;

  // Animated blobs
  blobs.forEach(b => {
    b.x += Math.sin(tick * b.dx * 100) * 0.001;
    b.y += Math.cos(tick * b.dy * 100) * 0.001;
    const grd = ctx.createRadialGradient(b.x * W, b.y * H, 0, b.x * W, b.y * H, b.r);
    grd.addColorStop(0, `rgba(${b.color},${b.alpha})`);
    grd.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.arc(b.x * W, b.y * H, b.r, 0, Math.PI * 2);
    ctx.fill();
  });

  drawConnections();
  particles.forEach(p => { p.update(); p.draw(); });
  requestAnimationFrame(animate);
}
animate();

// ── SCROLL REVEAL ────────────────────────────
const revealEls = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => entry.target.classList.add('visible'), i * 60);
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
revealEls.forEach(el => revealObserver.observe(el));

// ── COUNTER ANIMATION ────────────────────────
const counters = document.querySelectorAll('.stat-number');
let countersStarted = false;

const statsObserver = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting && !countersStarted) {
    countersStarted = true;
    counters.forEach(counter => {
      const target = +counter.dataset.target;
      const isCustom = isNaN(target);
      if (isCustom) return;
      let count = 0;
      const step = Math.ceil(target / 60);
      const timer = setInterval(() => {
        count = Math.min(count + step, target);
        counter.textContent = count + (counter.closest('.stat-card').querySelector('.stat-label').textContent.includes('%') ? '' : '+');
        if (count >= target) {
          counter.textContent = target + (counter.closest('.stat-card').querySelector('.stat-label').textContent.includes('%') ? '%' : '+');
          clearInterval(timer);
        }
      }, 25);
    });
  }
}, { threshold: 0.5 });

const statsSection = document.querySelector('.stats-section');
if (statsSection) statsObserver.observe(statsSection);

// ── PORTFOLIO FILTER ─────────────────────────
const filterBtns = document.querySelectorAll('.filter-btn');
const portfolioCards = document.querySelectorAll('.portfolio-card');

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const filter = btn.dataset.filter;
    portfolioCards.forEach(card => {
      if (filter === 'all' || card.dataset.category === filter) {
        card.style.display = '';
        setTimeout(() => card.style.opacity = '1', 10);
      } else {
        card.style.opacity = '0';
        setTimeout(() => card.style.display = 'none', 200);
      }
    });
  });
});

// ── CONTACT FORM ─────────────────────────────
const form       = document.getElementById('contactForm');
const submitBtn  = document.getElementById('submitBtn');
const successMsg = document.getElementById('formSuccess');
const errorMsg   = document.getElementById('formError');

// Primary endpoint: KD Technologies Django Backend with Brevo Transactional Email
const DJANGO_API_ENDPOINT = (window.location.protocol.startsWith('http') && window.location.port === '8000')
  ? '/api/contact/'
  : (window.location.protocol.startsWith('http') ? '/api/contact/' : 'http://127.0.0.1:8000/api/contact/');

// Fallback endpoint: Formspree (used if local Django server is offline)
const FORMSPREE_BACKUP_ENDPOINT = 'https://formspree.io/f/xvgaqrzn';

function validateField(input, errorId) {
  const error = document.getElementById(errorId);
  if (!input.value.trim()) {
    input.classList.add('error');
    error.textContent = 'This field is required.';
    return false;
  }
  if (input.type === 'email') {
    const emailReg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailReg.test(input.value.trim())) {
      input.classList.add('error');
      error.textContent = 'Please enter a valid email address.';
      return false;
    }
  }
  input.classList.remove('error');
  error.textContent = '';
  return true;
}

// Live validation on blur
document.getElementById('name').addEventListener('blur', () => validateField(document.getElementById('name'), 'nameError'));
document.getElementById('email').addEventListener('blur', () => validateField(document.getElementById('email'), 'emailError'));
document.getElementById('message').addEventListener('blur', () => validateField(document.getElementById('message'), 'messageError'));

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const nameOk    = validateField(document.getElementById('name'),    'nameError');
  const emailOk   = validateField(document.getElementById('email'),   'emailError');
  const messageOk = validateField(document.getElementById('message'), 'messageError');
  if (!nameOk || !emailOk || !messageOk) return;

  submitBtn.textContent = 'Sending… ⏳';
  submitBtn.disabled = true;
  successMsg.classList.remove('show');
  if (errorMsg) errorMsg.classList.remove('show');

  const payload = {
    name: document.getElementById('name').value.trim(),
    email: document.getElementById('email').value.trim(),
    service: document.getElementById('service') ? document.getElementById('service').value : '',
    budget: document.getElementById('budget') ? document.getElementById('budget').value : '',
    message: document.getElementById('message').value.trim(),
  };

  try {
    let response;
    let usingFallback = false;

    try {
      response = await fetch(DJANGO_API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
      });
    } catch (netErr) {
      // Local Django server not running -> fallback to Formspree
      console.warn('Django Brevo backend unreachable. Using backup endpoint...', netErr);
      usingFallback = true;
      const data = new FormData(form);
      response = await fetch(FORMSPREE_BACKUP_ENDPOINT, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      });
    }

    if (usingFallback) {
      if (response.ok) {
        form.reset();
        successMsg.textContent = "✅ Message sent! I'll get back to you within 24 hours.";
        successMsg.classList.add('show');
        setTimeout(() => successMsg.classList.remove('show'), 6000);
      } else {
        const json = await response.json();
        if (errorMsg) {
          errorMsg.textContent = json?.errors?.map(e => e.message).join(', ') || 'Something went wrong. Please try again.';
          errorMsg.classList.add('show');
          setTimeout(() => errorMsg.classList.remove('show'), 6000);
        }
      }
    } else {
      const result = await response.json();
      if (response.ok && result.success) {
        form.reset();
        successMsg.textContent = result.message || "✅ Message sent successfully! Check your inbox for confirmation.";
        successMsg.classList.add('show');
        setTimeout(() => successMsg.classList.remove('show'), 6000);
      } else {
        const errText = result.error || (result.field_errors ? Object.values(result.field_errors).join(', ') : 'Something went wrong. Please try again.');
        if (errorMsg) {
          errorMsg.textContent = errText;
          errorMsg.classList.add('show');
          setTimeout(() => errorMsg.classList.remove('show'), 8000);
        }
      }
    }
  } catch (err) {
    if (errorMsg) {
      errorMsg.textContent = 'Network error. Please check your connection and try again.';
      errorMsg.classList.add('show');
      setTimeout(() => errorMsg.classList.remove('show'), 6000);
    }
  } finally {
    submitBtn.textContent = 'Send Message 🚀';
    submitBtn.disabled = false;
  }
});

// ── SMOOTH SCROLL (for older browsers) ───────
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
