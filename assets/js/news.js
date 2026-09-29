/*
 * Lab news. Reads data/news.json and fills every element marked data-news.
 *   data-limit="3"     show only the newest N items (homepage)
 *   data-group="year"  group items under year headings (News page)
 * Each item in data/news.json: date (YYYY-MM-DD, YYYY-MM or YYYY), title,
 * and optionally text, link and link_label.
 */
(function () {
  var containers = document.querySelectorAll('[data-news]');
  if (!containers.length) return;

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];

  function formatDate(value) {
    var m = /^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?/.exec(String(value || ''));
    if (!m) return String(value || '');
    var year = m[1];
    if (!m[2]) return year;
    var month = MONTHS[parseInt(m[2], 10) - 1] || '';
    if (!m[3]) return month + ' ' + year;
    return month.slice(0, 3) + ' ' + parseInt(m[3], 10) + ', ' + year;
  }

  function safeLink(url) {
    url = String(url || '').trim();
    if (!url) return '';
    if (/^(https?:|mailto:)/i.test(url)) return url;
    if (/^[a-z][a-z0-9+.-]*:/i.test(url)) return '';
    return url;
  }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function buildItem(item, tag) {
    var node = el(tag, 'news-item');
    var time = el('time', 'news-date', formatDate(item.date));
    time.setAttribute('datetime', String(item.date));
    node.appendChild(time);
    var body = el('div', 'news-body');
    body.appendChild(el('h3', 'news-title', String(item.title)));
    if (item.text) body.appendChild(el('p', 'news-text', String(item.text)));
    var href = safeLink(item.link);
    if (href) {
      var a = el('a', 'text-link', String(item.link_label || 'Read more'));
      a.href = href;
      body.appendChild(a);
    }
    node.appendChild(body);
    return node;
  }

  function render(container, items) {
    container.textContent = '';
    var limit = parseInt(container.getAttribute('data-limit'), 10);
    var list = limit > 0 ? items.slice(0, limit) : items;
    var section = container.closest('[data-news-section]');

    if (!list.length) {
      if (section) section.hidden = true;
      else container.appendChild(el('p', 'news-status', 'No news yet.'));
      return;
    }

    if (container.getAttribute('data-group') === 'year') {
      var currentYear = null, ol = null;
      list.forEach(function (item) {
        var year = String(item.date).slice(0, 4);
        if (year !== currentYear) {
          currentYear = year;
          container.appendChild(el('h2', 'news-year', year));
          ol = el('ol', 'news-list');
          container.appendChild(ol);
        }
        ol.appendChild(buildItem(item, 'li'));
      });
    } else {
      list.forEach(function (item) { container.appendChild(buildItem(item, 'article')); });
    }
  }

  fetch('data/news.json', { cache: 'no-cache' })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      var items = (Array.isArray(data) ? data : [])
        .filter(function (item) { return item && item.date && item.title; })
        .sort(function (a, b) { return String(b.date).localeCompare(String(a.date)); });
      containers.forEach(function (c) { render(c, items); });
    })
    .catch(function (err) {
      console.error('Lab news could not be loaded. Check data/news.json.', err);
      containers.forEach(function (c) {
        var section = c.closest('[data-news-section]');
        if (section) { section.hidden = true; return; }
        c.textContent = '';
        c.appendChild(el('p', 'news-status', 'News could not be loaded right now.'));
      });
    });
})();
