// Brunna Rocha · Nutricionista — interações
document.addEventListener('DOMContentLoaded', function () {
  // Mobile menu
  var burger = document.querySelector('.burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      burger.classList.toggle('open');
      links.classList.toggle('open');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        burger.classList.remove('open');
        links.classList.remove('open');
      });
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-item button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      item.classList.toggle('open');
    });
  });

  // Reveal on scroll
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });

  // Header shadow on scroll
  var header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', function () {
      header.style.boxShadow = window.scrollY > 10 ? '0 10px 30px -14px rgba(0,0,0,.4)' : 'none';
    });
  }

  // Scrollspy: destaca o item de menu da seção visível (one-page)
  var anchorLinks = document.querySelectorAll('.nav-links a[href^="#"]');
  var sections = Array.prototype.slice.call(document.querySelectorAll('section[id]'));
  if (anchorLinks.length && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var id = e.target.getAttribute('id');
          anchorLinks.forEach(function (a) {
            a.classList.toggle('active', a.getAttribute('href') === '#' + id);
          });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });
  }

  // Blog: filtro por categoria + busca por tema
  var grid = document.getElementById('blogGrid');
  if (grid) {
    var items = Array.prototype.slice.call(grid.querySelectorAll('.blog-item'));
    var search = document.getElementById('blogSearch');
    var chips = document.getElementById('blogChips');
    var empty = document.getElementById('blogEmpty');
    var curCat = 'todos';
    function norm(s) { return (s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
    function applyFilter() {
      var q = norm(search && search.value ? search.value : '').trim();
      var visible = 0;
      items.forEach(function (it) {
        var okCat = curCat === 'todos' || it.getAttribute('data-cat') === curCat;
        var okQ = !q || norm(it.getAttribute('data-search') || '').indexOf(q) > -1;
        var show = okCat && okQ;
        it.style.display = show ? '' : 'none';
        if (show) visible++;
      });
      if (empty) empty.hidden = visible > 0;
    }
    if (search) search.addEventListener('input', applyFilter);
    if (chips) chips.addEventListener('click', function (e) {
      var b = e.target.closest('.blog-chip');
      if (!b) return;
      chips.querySelectorAll('.blog-chip').forEach(function (x) { x.classList.remove('active'); });
      b.classList.add('active');
      curCat = b.getAttribute('data-cat');
      applyFilter();
    });
  }

  // Transição de página: fade suave ao clicar em links internos
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href) return;
    if (a.target === '_blank' || a.hasAttribute('download')) return;
    if (/^(https?:|mailto:|tel:|#|javascript:)/i.test(href)) return;
    // navegação interna (mesma origem, arquivo .html ou relativo)
    e.preventDefault();
    document.body.classList.add('page-leaving');
    setTimeout(function () { window.location.href = href; }, 250);
  });
});
