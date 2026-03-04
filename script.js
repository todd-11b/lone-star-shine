/* ========================================
   LONE STAR SHINE — script.js
   ======================================== */

(function () {
  'use strict';

  // ── Mobile Navigation ──
  const mobileToggle = document.querySelector('.mobile-toggle');
  const mobileNav = document.getElementById('mobile-nav');

  if (mobileToggle && mobileNav) {
    mobileToggle.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('active');
      mobileToggle.classList.toggle('active');
      mobileToggle.setAttribute('aria-expanded', isOpen);
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close mobile nav when a link is clicked
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('active');
        mobileToggle.classList.remove('active');
        mobileToggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  // ── Sticky Header — hide offer bar on scroll ──
  var lastScroll = 0;
  var header = document.getElementById('header');
  var offerBar = document.querySelector('.offer-bar');

  if (header && offerBar) {
    window.addEventListener('scroll', function () {
      var scrollY = window.scrollY;
      if (scrollY > 60) {
        offerBar.style.marginTop = '-' + offerBar.offsetHeight + 'px';
      } else {
        offerBar.style.marginTop = '0';
      }
      lastScroll = scrollY;
    }, { passive: true });

    offerBar.style.transition = 'margin-top 0.3s ease';
  }

  // ── Price Estimator ──
  var bedSlider = document.getElementById('bedrooms');
  var bathSlider = document.getElementById('bathrooms');
  var bedValue = document.getElementById('bed-value');
  var bathValue = document.getElementById('bath-value');
  var typeButtons = document.querySelectorAll('.type-btn');
  var freqSelect = document.getElementById('frequency');
  var priceDisplay = document.getElementById('estimate-price');

  var estimatorState = {
    bedrooms: 3,
    bathrooms: 2,
    typeMultiplier: 1.0,
    freqDiscount: 1.0
  };

  function calculateEstimate() {
    var base = 109;
    var bedAdd = estimatorState.bedrooms * 15;
    var bathAdd = estimatorState.bathrooms * 25;
    var subtotal = (base + bedAdd + bathAdd) * estimatorState.typeMultiplier * estimatorState.freqDiscount;
    var low = Math.round(subtotal * 0.9);
    var high = Math.round(subtotal * 1.1);
    if (priceDisplay) {
      priceDisplay.textContent = '$' + low + ' – $' + high;
    }
  }

  if (bedSlider) {
    bedSlider.addEventListener('input', function () {
      estimatorState.bedrooms = parseInt(this.value);
      if (bedValue) bedValue.textContent = this.value;
      calculateEstimate();
    });
  }

  if (bathSlider) {
    bathSlider.addEventListener('input', function () {
      estimatorState.bathrooms = parseInt(this.value);
      if (bathValue) bathValue.textContent = this.value;
      calculateEstimate();
    });
  }

  typeButtons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      typeButtons.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');
      estimatorState.typeMultiplier = parseFloat(this.dataset.mult);
      calculateEstimate();
    });
  });

  if (freqSelect) {
    freqSelect.addEventListener('change', function () {
      estimatorState.freqDiscount = parseFloat(this.value);
      calculateEstimate();
    });
  }

  // Initial calculation
  calculateEstimate();

  // ── FAQ Accordion ──
  var faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(function (item) {
    var question = item.querySelector('.faq-question');
    var answer = item.querySelector('.faq-answer');

    if (question && answer) {
      question.addEventListener('click', function () {
        var isActive = item.classList.contains('active');

        // Close all
        faqItems.forEach(function (fi) {
          fi.classList.remove('active');
          var a = fi.querySelector('.faq-answer');
          var q = fi.querySelector('.faq-question');
          if (a) a.style.maxHeight = null;
          if (q) q.setAttribute('aria-expanded', 'false');
        });

        // Open clicked (if it wasn't already open)
        if (!isActive) {
          item.classList.add('active');
          answer.style.maxHeight = answer.scrollHeight + 'px';
          question.setAttribute('aria-expanded', 'true');
        }
      });
    }
  });

  // ── Form Validation & Submission ──
  var quoteForm = document.getElementById('quote-form');
  var formSuccess = document.getElementById('form-success');

  if (quoteForm) {
    quoteForm.addEventListener('submit', function (e) {
      e.preventDefault();

      // Reset errors
      quoteForm.querySelectorAll('.form-group').forEach(function (g) {
        g.classList.remove('has-error');
      });
      quoteForm.querySelectorAll('input, select, textarea').forEach(function (el) {
        el.classList.remove('error');
      });

      var valid = true;

      // Validate required fields
      var name = document.getElementById('q-name');
      var email = document.getElementById('q-email');
      var phone = document.getElementById('q-phone');

      if (!name.value.trim()) {
        markError(name);
        valid = false;
      }

      if (!email.value.trim() || !isValidEmail(email.value)) {
        markError(email);
        valid = false;
      }

      if (!phone.value.trim()) {
        markError(phone);
        valid = false;
      }

      if (!valid) return;

      // Collect form data
      var formData = {
        name: name.value.trim(),
        email: email.value.trim(),
        phone: phone.value.trim(),
        city: document.getElementById('q-city').value.trim(),
        zip: document.getElementById('q-zip').value.trim(),
        bedrooms: document.getElementById('q-bedrooms').value,
        bathrooms: document.getElementById('q-bathrooms').value,
        service: document.getElementById('q-service').value,
        frequency: document.getElementById('q-frequency').value,
        date: document.getElementById('q-date').value,
        notes: document.getElementById('q-notes').value.trim(),
        sms_consent: document.getElementById('q-sms').checked
      };

      console.log('Quote Request Submitted:', formData);

      // Show success
      quoteForm.style.display = 'none';
      if (formSuccess) formSuccess.style.display = 'block';
    });
  }

  function markError(input) {
    input.classList.add('error');
    var group = input.closest('.form-group');
    if (group) group.classList.add('has-error');
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // ── Scroll Animations (Intersection Observer) ──
  var animateElements = document.querySelectorAll(
    '.service-card, .step, .pricing-card, .trust-card, .review-card, .ba-card, .proof-card'
  );

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    animateElements.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(24px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      observer.observe(el);
    });
  }

  // ── Active Nav Highlight ──
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav-links a:not(.btn)');

  if (sections.length && navLinks.length) {
    window.addEventListener('scroll', function () {
      var scrollPos = window.scrollY + 120;

      sections.forEach(function (section) {
        var top = section.offsetTop;
        var height = section.offsetHeight;
        var id = section.getAttribute('id');

        if (scrollPos >= top && scrollPos < top + height) {
          navLinks.forEach(function (link) {
            link.style.color = '';
            if (link.getAttribute('href') === '#' + id) {
              link.style.color = '#2FA4A9';
            }
          });
        }
      });
    }, { passive: true });
  }

})();
