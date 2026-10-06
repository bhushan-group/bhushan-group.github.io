/*
 * Lab members. Reads data/people.json and fills the element marked
 * data-people. Each entry has a name and a group, and optionally a role,
 * program, bio, photo, linkedin, scholar, github and show. Entries with
 * "show": false are hidden, which is how someone is parked without being
 * deleted. Anyone without a photo gets their initials instead, at the same
 * size, so the rows stay even.
 */
(function () {
  var mount = document.querySelector('[data-people]');
  if (!mount) return;

  // Groups appear in this order; anything else is appended in the order met.
  var ORDER = ['Research staff', 'PhD students', "Master's students",
    'Undergraduate researchers', 'Visiting researchers'];

  var LINKS = [
    { key: 'linkedin', label: 'LinkedIn' },
    { key: 'scholar', label: 'Google Scholar' },
    { key: 'github', label: 'GitHub' }
  ];

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  // Links: web only. Photos: web, or a file on this site.
  function safeUrl(url, allowExternalOnly) {
    url = String(url || '').trim();
    if (!url) return '';
    if (/^https?:\/\//i.test(url)) return url;
    if (allowExternalOnly) return '';
    if (/^[a-z][a-z0-9+.-]*:/i.test(url) || url.indexOf('//') === 0) return '';
    return url.replace(/^\/+/, '');
  }

  function initials(name) {
    var parts = String(name || '').trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return '?';
    if (parts.length === 1) return parts[0].slice(0, 1).toUpperCase();
    return (parts[0].slice(0, 1) + parts[parts.length - 1].slice(0, 1)).toUpperCase();
  }

  function avatar(person) {
    var box = el('span', 'avatar avatar-person');
    var src = safeUrl(person.photo, false);
    if (!src) {
      box.textContent = initials(person.name);
      box.setAttribute('aria-hidden', 'true');
      return box;
    }
    var img = document.createElement('img');
    img.src = src;
    img.alt = String(person.name || '');
    img.loading = 'lazy';
    img.width = 88;
    img.height = 88;
    // A missing file would otherwise leave a blank circle.
    img.onerror = function () {
      box.textContent = initials(person.name);
      box.setAttribute('aria-hidden', 'true');
    };
    box.appendChild(img);
    return box;
  }

  function card(person) {
    var node = el('article', 'person');
    node.appendChild(avatar(person));
    var body = el('div', 'person-body');
    body.appendChild(el('h3', null, String(person.name || '')));

    var role = [person.role, person.program].filter(function (x) {
      return String(x || '').trim();
    }).join(', ');
    if (role) body.appendChild(el('p', 'person-role', role));

    if (person.bio) body.appendChild(el('p', 'bio', String(person.bio)));

    var row = el('p', 'person-links');
    LINKS.forEach(function (link) {
      var href = safeUrl(person[link.key], true);
      if (!href) return;
      var a = el('a', null, link.label);
      a.href = href;
      a.rel = 'noopener';
      // Screen readers hear a list of identical "LinkedIn" links otherwise.
      a.setAttribute('aria-label', link.label + ' profile of ' + String(person.name || ''));
      row.appendChild(a);
    });
    if (row.childNodes.length) body.appendChild(row);

    node.appendChild(body);
    return node;
  }

  function render(people) {
    mount.textContent = '';
    if (!people.length) {
      mount.appendChild(el('p', 'news-status', 'Lab members are being updated.'));
      return;
    }
    var groups = [];
    var byName = {};
    people.forEach(function (person) {
      var name = String(person.group || 'Lab members');
      if (!byName[name]) { byName[name] = []; groups.push(name); }
      byName[name].push(person);
    });
    groups.sort(function (a, b) {
      var ia = ORDER.indexOf(a), ib = ORDER.indexOf(b);
      if (ia === -1 && ib === -1) return groups.indexOf(a) - groups.indexOf(b);
      if (ia === -1) return 1;
      if (ib === -1) return -1;
      return ia - ib;
    });
    groups.forEach(function (name) {
      var block = el('div', 'people-group');
      block.appendChild(el('h2', null, name));
      var grid = el('div', 'people-grid');
      byName[name].forEach(function (person) { grid.appendChild(card(person)); });
      block.appendChild(grid);
      mount.appendChild(block);
    });
  }

  fetch('data/people.json', { cache: 'no-cache' })
    .then(function (response) {
      if (!response.ok) throw new Error('HTTP ' + response.status);
      return response.json();
    })
    .then(function (data) {
      render((Array.isArray(data) ? data : []).filter(function (person) {
        return person && person.name && person.show !== false;
      }));
    })
    .catch(function (err) {
      console.error('Lab members could not be loaded. Check data/people.json.', err);
      mount.textContent = '';
      mount.appendChild(el('p', 'news-status',
        'The list of lab members could not be loaded right now.'));
    });
})();
