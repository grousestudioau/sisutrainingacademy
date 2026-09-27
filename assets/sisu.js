// SISU: shared behaviour for every page.
(function () {
  var yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // One fade, once.
  var io = 'IntersectionObserver' in window && new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal').forEach(function (el) { io ? io.observe(el) : el.classList.add('in'); });

  // Forms: <form data-endpoint="https://formspree.io/f/..."> followed by a .form-done block.
  document.querySelectorAll('form[data-endpoint]').forEach(function (form) {
    var btn = form.querySelector('button[type="submit"]');
    var label = btn.textContent;
    var err = form.querySelector('.form-error');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      btn.disabled = true; btn.textContent = 'Sending…';
      if (err) err.hidden = true;
      fetch(form.dataset.endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.hidden = true;
          var done = form.nextElementSibling;
          if (done && done.classList.contains('form-done')) { done.hidden = false; done.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
        })
        .catch(function () {
          if (err) err.hidden = false;
          btn.disabled = false; btn.textContent = label;
        });
    });
  });
})();
