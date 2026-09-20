(() => {
  const sidebar = document.querySelector('#sidebar');
  const toggle = document.querySelector('[data-sidebar-toggle]');

  const closeSidebar = () => {
    if (!sidebar || !toggle) return;
    sidebar.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  };

  toggle?.addEventListener('click', () => {
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
    if (!sidebar?.classList.contains('is-open') || !toggle) return;
    if (!sidebar.contains(event.target) && !toggle.contains(event.target)) closeSidebar();
  });

  const consentCheckbox = document.querySelector('[data-consent-checkbox]');
  const consentSubmit = document.querySelector('[data-consent-submit]');
  if (consentCheckbox && consentSubmit) {
    const syncConsent = () => { consentSubmit.disabled = !consentCheckbox.checked; };
    consentCheckbox.addEventListener('change', syncConsent);
    syncConsent();
  }

  document.querySelectorAll('.select-row input[type="checkbox"]').forEach((input) => {
    input.addEventListener('change', () => input.closest('.select-row')?.classList.toggle('selected', input.checked));
  });
})();

