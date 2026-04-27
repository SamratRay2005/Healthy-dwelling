/* Healthy dwelling — Client-side JS */

// ── Hero Carousel ──────────────────────────────────────────────────────────
(function () {
  const carousel = document.getElementById("hero-carousel");
  const dotsContainer = document.getElementById("carousel-dots");
  if (!carousel || !dotsContainer) return;

  const slides = carousel.querySelectorAll(".hero-slide");
  const dots   = dotsContainer.querySelectorAll(".carousel-dot");
  if (slides.length <= 1) return;

  let current = 0;
  let timer;

  function goTo(index) {
    slides[current].classList.remove("active");
    dots[current].classList.remove("active");
    current = (index + slides.length) % slides.length;
    slides[current].classList.add("active");
    dots[current].classList.add("active");
  }

  function advance() { goTo(current + 1); }

  function startTimer() {
    clearInterval(timer);
    timer = setInterval(advance, 5000);
  }

  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => { goTo(i); startTimer(); });
  });

  // Keyboard
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") { goTo(current + 1); startTimer(); }
    if (e.key === "ArrowLeft")  { goTo(current - 1); startTimer(); }
  });

  // Touch swipe
  let touchStartX = 0;
  carousel.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
  carousel.addEventListener("touchend", (e) => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) { goTo(current + (diff > 0 ? 1 : -1)); startTimer(); }
  });

  startTimer();
})();

// ── Mobile Nav Toggle ─────────────────────────────────────────────────────
(function () {
  const toggle = document.getElementById("nav-toggle");
  const nav    = document.getElementById("main-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open);
    // Animate hamburger to X
    const spans = toggle.querySelectorAll("span");
    if (open) {
      spans[0].style.transform = "translateY(7px) rotate(45deg)";
      spans[1].style.opacity = "0";
      spans[2].style.transform = "translateY(-7px) rotate(-45deg)";
    } else {
      spans[0].style.transform = "";
      spans[1].style.opacity = "";
      spans[2].style.transform = "";
    }
  });

  // Close on link click
  nav.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
      nav.classList.remove("open");
      toggle.setAttribute("aria-expanded", false);
    });
  });
})();

// ── Subscribe Form ────────────────────────────────────────────────────────
function handleSubscribe(e) {
  e.preventDefault();
  const form  = e.target;
  const input = form.querySelector("input[type=email]");
  const btn   = form.querySelector("button");
  if (!input.value) return;

  btn.textContent = "✓ Subscribed!";
  btn.disabled = true;
  btn.style.background = "var(--sage)";
  input.value = "";

  setTimeout(() => {
    btn.textContent = "Subscribe";
    btn.disabled = false;
    btn.style.background = "";
  }, 3000);
}

// ── Smooth scroll for anchor links ────────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener("click", (e) => {
    const target = document.querySelector(a.getAttribute("href"));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: "smooth" }); }
  });
});

// ── Animate cards on scroll (Intersection Observer) ───────────────────────
(function () {
  if (!window.IntersectionObserver) return;
  const cards = document.querySelectorAll(".article-card, .category-card");

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = "fadeSlideUp 0.45s ease both";
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  // Inject keyframe
  if (!document.getElementById("anim-style")) {
    const style = document.createElement("style");
    style.id = "anim-style";
    style.textContent = `
      @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
      }
    `;
    document.head.appendChild(style);
  }

  cards.forEach((card, i) => {
    card.style.opacity = "0";
    card.style.animationDelay = `${i * 0.07}s`;
    observer.observe(card);
  });
})();
