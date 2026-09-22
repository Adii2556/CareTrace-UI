(() => {
  const getSidebar = () => document.querySelector('#sidebar');
  const getToggle = () => document.querySelector('[data-sidebar-toggle]');

  const closeSidebar = () => {
    const sidebar = getSidebar();
    const toggle = getToggle();
    if (!sidebar || !toggle) return;
    sidebar.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  const navFromPath = (value = window.location.pathname) => {
    const path = new URL(value, window.location.origin).pathname;
    if (path.startsWith('/timeline/')) return 'timeline';
    if (path.startsWith('/records/') && path.endsWith('/explain/')) return 'explain';
    if (path.startsWith('/records/')) return 'records';
    if (path.startsWith('/referrals/')) return 'referrals';
    if (path.startsWith('/privacy/')) return 'privacy';
    if (path.startsWith('/profile/')) return 'profile';
    return 'dashboard';
  };

  const syncActiveNavigation = (activeOverride = '') => {
    const main = document.querySelector('#app-content');
    const activeNav = activeOverride || main?.dataset.activeNav || navFromPath();
    document.body.dataset.page = activeNav;
    document.querySelectorAll('[data-nav]').forEach((link) => {
      const isActive = Boolean(activeNav) && link.dataset.nav === activeNav;
      link.classList.toggle('active', isActive);
      if (isActive) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  };

  const initContent = (root = document) => {
    const consentCheckbox = root.querySelector('[data-consent-checkbox]');
    const consentSubmit = root.querySelector('[data-consent-submit]');
    if (consentCheckbox && consentSubmit && !consentCheckbox.dataset.caretraceBound) {
      const syncConsent = () => { consentSubmit.disabled = !consentCheckbox.checked; };
      consentCheckbox.addEventListener('change', syncConsent);
      consentCheckbox.dataset.caretraceBound = 'true';
      syncConsent();
    }

    root.querySelectorAll('.select-row input[type="checkbox"]').forEach((input) => {
      if (input.dataset.caretraceBound) return;
      input.addEventListener('change', () => {
        input.closest('.select-row')?.classList.toggle('selected', input.checked);
      });
      input.dataset.caretraceBound = 'true';
    });

    const recordModal = root.querySelector('#recordModal');
    if (recordModal && window.location.hash === '#add-record' && window.bootstrap) {
      window.bootstrap.Modal.getOrCreateInstance(recordModal).show();
    }
  };

  getToggle()?.addEventListener('click', () => {
    const sidebar = getSidebar();
    const toggle = getToggle();
    if (!sidebar || !toggle) return;
    const open = sidebar.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeSidebar();
    if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
      const search = document.querySelector('input[type="search"], input[name="q"]');
      if (search) {
        event.preventDefault();
        search.focus();
      }
    }
  });

  document.addEventListener('click', (event) => {
    const sidebar = getSidebar();
    const toggle = getToggle();
    if (event.target.closest('.app-navigation a')) closeSidebar();
    if (!sidebar?.classList.contains('is-open') || !toggle) return;
    if (!sidebar.contains(event.target) && !toggle.contains(event.target)) closeSidebar();
  });

  document.addEventListener('htmx:beforeRequest', () => {
    document.querySelector('#app-content')?.setAttribute('aria-busy', 'true');
  });

  document.addEventListener('htmx:afterRequest', () => {
    document.querySelector('#app-content')?.removeAttribute('aria-busy');
  });

  document.addEventListener('htmx:afterSwap', (event) => {
    const target = event.detail?.target;
    const main = target?.matches?.('#app-content')
      ? target
      : document.querySelector('#app-content');
    initContent(main || document);
    syncActiveNavigation();
    main?.focus({ preventScroll: true });
  });

  document.addEventListener('htmx:historyRestore', (event) => {
    initContent(document.querySelector('#app-content') || document);
    syncActiveNavigation(navFromPath(event.detail.path));
  });

  window.addEventListener('popstate', () => syncActiveNavigation(navFromPath()));

  initContent();
  syncActiveNavigation();
})();
