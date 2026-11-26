// Title filter for the patterns index (/patterns). Loaded through the page's
// `scripts` frontmatter, so Flowershow runs it each time the page is shown.
(function () {
  if (document.currentScript && !document.currentScript.isConnected) return;
  var rows = Array.prototype.slice.call(document.querySelectorAll('table tbody tr'))
    .filter(function (tr) { return tr.querySelector('a[href*="/patterns/"]'); });
  var heading = document.querySelector('h1');
  if (!rows.length || !heading || document.querySelector('.pattern-filter')) return;

  var fold = function (s) {
    return s.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  };
  var items = rows.map(function (tr) {
    var cells = tr.querySelectorAll('td');
    return { tr: tr, num: cells[0].textContent.trim(), title: fold(cells[1].textContent), link: tr.querySelector('a') };
  });

  var input = document.createElement('input');
  input.type = 'search';
  input.className = 'pattern-filter';
  input.placeholder = 'Find a pattern by name or number';
  input.setAttribute('aria-label', 'Find a pattern by name or number');
  input.autocomplete = 'off';
  var count = document.createElement('p');
  count.className = 'pattern-filter-count';
  count.setAttribute('aria-live', 'polite');
  var list = document.createElement('ul');
  list.className = 'pattern-filter-results';
  heading.insertAdjacentElement('afterend', input);
  input.insertAdjacentElement('afterend', count);
  count.insertAdjacentElement('afterend', list);

  var shown = items;
  var update = function () {
    var q = fold(input.value);
    var words = q ? q.split(' ') : [];
    shown = items.filter(function (it) {
      if (!words.length) return true;
      if (/^\d+$/.test(q)) return it.num === q;
      return words.every(function (w) { return it.title.indexOf(w) !== -1; });
    });
    items.forEach(function (it) { it.tr.hidden = shown.indexOf(it) === -1; });
    document.querySelectorAll('table').forEach(function (t) {
      var any = t.querySelector('tbody tr:not([hidden])');
      t.hidden = !any && words.length > 0;
    });
    list.innerHTML = '';
    if (words.length) shown.slice(0, 12).forEach(function (it) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = it.link.getAttribute('href');
      var n = document.createElement('span');
      n.className = 'pl-num';
      n.textContent = it.num;
      a.appendChild(n);
      a.appendChild(document.createTextNode(' ' + it.link.textContent));
      li.appendChild(a);
      list.appendChild(li);
    });
    count.textContent = words.length ? (shown.length === 1 ? '1 pattern · press Enter to open' : shown.length + ' patterns' + (shown.length > 12 ? ' · first 12 below, all in the index' : '')) : '';
  };
  input.addEventListener('input', update);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && shown.length === 1 && input.value) { shown[0].link.click(); }
    if (e.key === 'Escape') { input.value = ''; update(); }
  });
})();
