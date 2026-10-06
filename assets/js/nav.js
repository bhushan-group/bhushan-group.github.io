/*
 * Header dropdown menus. Any <li class="nav-menu"> holding a button and a
 * <ul class="nav-menu-list"> becomes a menu that opens on click, closes on
 * Escape, on a click elsewhere, and when focus leaves it. If this file never
 * runs, the stylesheet hides the button and shows the links as plain nav
 * items, so nothing in the menu becomes unreachable.
 */
(function () {
  var menus = document.querySelectorAll('.nav-menu');
  if (!menus.length) return;

  var open = null;

  function close(menu) {
    if (!menu) return;
    menu.button.setAttribute('aria-expanded', 'false');
    menu.list.hidden = true;
    if (open === menu) open = null;
  }

  function show(menu) {
    if (open && open !== menu) close(open);
    menu.button.setAttribute('aria-expanded', 'true');
    menu.list.hidden = false;
    open = menu;
  }

  Array.prototype.forEach.call(menus, function (root) {
    var button = root.querySelector('.nav-menu-btn');
    var list = root.querySelector('.nav-menu-list');
    if (!button || !list) return;
    var menu = { root: root, button: button, list: list };

    // Scripting is on, so the list starts closed.
    list.hidden = true;
    button.setAttribute('aria-expanded', 'false');

    button.addEventListener('click', function () {
      if (button.getAttribute('aria-expanded') === 'true') close(menu);
      else show(menu);
    });

    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && open === menu) {
        close(menu);
        button.focus();
      }
    });

    // Closing on focusout lets keyboard users tab straight past the menu.
    root.addEventListener('focusout', function () {
      window.setTimeout(function () {
        if (open === menu && !root.contains(document.activeElement)) close(menu);
      }, 0);
    });
  });

  document.addEventListener('click', function (e) {
    if (open && !open.root.contains(e.target)) close(open);
  });
})();
