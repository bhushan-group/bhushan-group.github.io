/*
 * Lab news. Reads data/news.json and fills every element marked data-news.
 *   data-layout="strip"    horizontally scrolling cards (homepage)
 *   data-layout="archive"  items grouped under year headings, with filters
 *                          by type and links to each year (News page)
 *   data-limit="8"         show only the newest N items
 * Each item in data/news.json has a date (2026-09-24, 2026-09 or 2026) and a
 * title, and optionally: text, category (Paper, Talk, Award, People, Grant,
 * Event, Media or Lab), image, image_alt, link, link_label,
 * show. Items with "show": false are drafts and are not displayed.
 */
(function () {
  var containers = document.querySelectorAll('[data-news]');
  if (!containers.length) return;

  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];

  var CATEGORIES = {
    paper: { label: 'Paper', icon: ['M7 3h7l5 5v13H7z', 'M14 3v5h5', 'M10 12h6', 'M10 16h6'] },
    talk: { label: 'Talk', icon: ['M3 4h18', 'M4 4v10h16V4', 'M12 14v4', 'M8 21l4-3 4 3'] },
    award: { label: 'Award', icon: ['M12 3a5 5 0 1 0 0 10a5 5 0 1 0 0-10z', 'M9 12.5L7.5 21l4.5-2.5 4.5 2.5L15 12.5'] },
    people: { label: 'People', icon: ['M9 5a3 3 0 1 0 0 6a3 3 0 1 0 0-6z', 'M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6', 'M17 6.5a2.5 2.5 0 1 0 0 5a2.5 2.5 0 1 0 0-5z', 'M16 14.2c2.8.3 5 2.6 5 5.8'] },
    grant: { label: 'Grant', icon: ['M12 21v-9', 'M12 12c0-4-3-6-7-6 0 4 3 6 7 6z', 'M12 10c0-3 2.5-5 6-5 0 3-2.5 5-6 5z'] },
    event: { label: 'Event', icon: ['M5 5h14a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2z', 'M3 10h18', 'M8 3v4', 'M16 3v4'] },
    media: { label: 'Media', icon: ['M4 5h13v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z', 'M17 9h3v10a2 2 0 0 1-2 2', 'M7 9h7', 'M7 13h7', 'M7 17h4'] },
    lab: { label: 'Lab', icon: ['M9 3h6', 'M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3', 'M7.5 15h9'] }
  };

  function category(item) {
    var key = String(item.category || '').trim().toLowerCase();
    return CATEGORIES[key] ? key : 'lab';
  }

  function formatDate(value) {
    var m = /^(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?/.exec(String(value || ''));
    if (!m) return String(value || '');
    var year = m[1];
    if (!m[2]) return year;
    var month = MONTHS[parseInt(m[2], 10) - 1] || '';
    if (!m[3]) return month + ' ' + year;
    return month.slice(0, 3) + ' ' + parseInt(m[3], 10) + ', ' + year;
  }

  // Links: web, email or a page on this site. Images: web or a file on this site.
  function safeUrl(url, allowMail) {
    url = String(url || '').trim();
    if (!url) return '';
    if (/^https?:\/\//i.test(url)) return url;
    if (allowMail && /^mailto:/i.test(url)) return url;
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.indexOf('//') === 0) return '';
    return url.replace(/^\/+/, '');
  }

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function glyph(key, size, className) {
    var ns = 'http://www.w3.org/2000/svg';
    var box = el('div', className || 'news-glyph');
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('width', String(size || 56));
    svg.setAttribute('height', String(size || 56));
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', size && size < 40 ? '1.7' : '1.4');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');
    CATEGORIES[key].icon.forEach(function (d) {
      var path = document.createElementNS(ns, 'path');
      path.setAttribute('d', d);
      svg.appendChild(path);
    });
    box.appendChild(svg);
    return box;
  }

  function media(item, key) {
    var wrap = el('div', 'news-media');
    var src = safeUrl(item.image, false);
    if (src) {
      var img = document.createElement('img');
      img.src = src;
      img.alt = String(item.image_alt || '');
      img.loading = 'lazy';
      img.onerror = function () { wrap.textContent = ''; wrap.appendChild(glyph(key)); };
      wrap.appendChild(img);
    } else {
      wrap.appendChild(glyph(key));
    }
    return wrap;
  }

  function meta(item, key) {
    var row = el('p', 'news-meta');
    row.appendChild(el('span', 'news-chip', CATEGORIES[key].label));
    var time = el('time', 'news-date', formatDate(item.date));
    time.setAttribute('datetime', String(item.date));
    row.appendChild(time);
    return row;
  }

  function link(item) {
    var href = safeUrl(item.link, true);
    if (!href) return null;
    var a = el('a', 'text-link', String(item.link_label || 'Read more'));
    a.href = href;
    return a;
  }

  function card(item) {
    var key = category(item);
    var node = el('article', 'news-card cat-' + key);
    node.appendChild(media(item, key));
    var body = el('div', 'news-card-body');
    body.appendChild(meta(item, key));
    body.appendChild(el('h3', 'news-title', String(item.title)));
    if (item.text) body.appendChild(el('p', 'news-text', String(item.text)));
    var a = link(item);
    if (a) body.appendChild(a);
    node.appendChild(body);
    return node;
  }

  function row(item) {
    var key = category(item);
    var node = el('li', 'news-row cat-' + key);
    node.appendChild(glyph(key, 24, 'news-icon'));
    var body = el('div', 'news-body');
    body.appendChild(meta(item, key));
    body.appendChild(el('h3', 'news-title', String(item.title)));
    if (item.text) body.appendChild(el('p', 'news-text', String(item.text)));
    var a = link(item);
    if (a) body.appendChild(a);
    node.appendChild(body);
    var src = safeUrl(item.image, false);
    if (src) {
      var thumb = el('div', 'news-thumb');
      var img = document.createElement('img');
      img.src = src;
      img.alt = String(item.image_alt || '');
      img.loading = 'lazy';
      img.onerror = function () { thumb.remove(); node.classList.remove('has-image'); };
      thumb.appendChild(img);
      node.appendChild(thumb);
      node.classList.add('has-image');
    }
    return node;
  }

  function setUpScrollButtons(track) {
    if (!track.id) return;
    var buttons = document.querySelectorAll('[data-scroll][aria-controls="' + track.id + '"]');
    if (!buttons.length) return;
    function update() {
      var max = track.scrollWidth - track.clientWidth - 8;
      buttons.forEach(function (b) {
        var back = b.getAttribute('data-scroll') === 'prev';
        b.disabled = back ? track.scrollLeft <= 8 : track.scrollLeft >= max;
      });
    }
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var step = Math.max(track.clientWidth * 0.8, 280);
        track.scrollBy({ left: b.getAttribute('data-scroll') === 'prev' ? -step : step });
      });
    });
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  function archive(container, items) {
    var side = el('div', 'news-side');
    var main = el('div', 'news-main');

    var typeLabel = el('p', 'news-side-h', 'Type');
    typeLabel.id = 'news-type-label';
    var filters = el('div', 'news-filters');
    filters.setAttribute('role', 'group');
    filters.setAttribute('aria-labelledby', 'news-type-label');

    var yearLabel = el('p', 'news-side-h', 'Year');
    yearLabel.id = 'news-year-label';
    var years = el('nav', 'news-years');
    years.setAttribute('aria-labelledby', 'news-year-label');

    var count = el('p', 'news-count');
    count.setAttribute('aria-live', 'polite');
    var list = el('div', 'news-groups');

    var typeBlock = el('div', 'news-side-block');
    typeBlock.appendChild(typeLabel);
    typeBlock.appendChild(filters);
    var yearBlock = el('div', 'news-side-block');
    yearBlock.appendChild(yearLabel);
    yearBlock.appendChild(years);
    side.appendChild(typeBlock);
    side.appendChild(yearBlock);
    main.appendChild(count);
    main.appendChild(list);
    container.appendChild(side);
    container.appendChild(main);

    var totals = {};
    items.forEach(function (item) { var k = category(item); totals[k] = (totals[k] || 0) + 1; });

    function button(key, label, n) {
      var b = el('button', 'news-filter' + (key ? ' cat-' + key : ''));
      b.type = 'button';
      b.setAttribute('data-filter', key);
      b.appendChild(document.createTextNode(label + ' '));
      b.appendChild(el('span', 'news-filter-n', String(n)));
      b.addEventListener('click', function () { draw(key); });
      filters.appendChild(b);
    }
    button('', 'All', items.length);
    Object.keys(CATEGORIES).forEach(function (k) {
      if (totals[k]) button(k, CATEGORIES[k].label, totals[k]);
    });

    function draw(key) {
      filters.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', b.getAttribute('data-filter') === key ? 'true' : 'false');
      });
      var shown = key ? items.filter(function (i) { return category(i) === key; }) : items;
      list.textContent = '';
      years.textContent = '';
      var currentYear = null, ol = null;
      shown.forEach(function (item) {
        var year = String(item.date).slice(0, 4);
        if (year !== currentYear) {
          currentYear = year;
          var h = el('h2', 'news-year', year);
          h.id = 'news-' + year;
          h.tabIndex = -1;
          list.appendChild(h);
          ol = el('ol', 'news-list');
          list.appendChild(ol);
          var a = el('a', 'news-year-link', year);
          a.href = '#news-' + year;
          years.appendChild(a);
        }
        ol.appendChild(row(item));
      });
      count.textContent = key
        ? 'Showing ' + shown.length + ' of ' + items.length + ' items: ' + CATEGORIES[key].label
        : items.length + ' items, newest first';
    }
    draw('');
    var target = location.hash && document.getElementById(location.hash.slice(1));
    if (target) target.scrollIntoView();
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

    if (container.getAttribute('data-layout') === 'archive') {
      archive(container, list);
    } else {
      list.forEach(function (item) { container.appendChild(card(item)); });
      setUpScrollButtons(container);
    }
  }

  fetch('data/news.json', { cache: 'no-cache' })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      var items = (Array.isArray(data) ? data : [])
        .filter(function (item) { return item && item.date && item.title && item.show !== false; })
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
