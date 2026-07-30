document.addEventListener('DOMContentLoaded', () => {
  const filters = Array.from(document.querySelectorAll('[data-history-filter]'));
  const branches = Array.from(document.querySelectorAll('[data-history-branches]'));

  if (!filters.length || !branches.length) {
    return;
  }

  const statusMatches = (status, filter) => {
    if (filter === 'all') {
      return true;
    }
    if (filter === 'active') {
      return status === 'open' || status === 'accepted';
    }
    if (filter === 'resolved') {
      return status === 'accepted' || status === 'rejected' || status === 'outdated';
    }
    return status === filter;
  };

  const applyFilter = (filter) => {
    filters.forEach((button) => {
      const isActive = button.dataset.historyFilter === filter;
      button.classList.toggle('active', isActive);
      button.setAttribute('aria-pressed', String(isActive));
    });

    branches.forEach((branch) => {
      const suggestions = Array.from(
        branch.querySelectorAll('[data-history-suggestion]'),
      );
      let visibleCount = 0;

      suggestions.forEach((suggestion) => {
        const isVisible = statusMatches(
          suggestion.dataset.suggestionStatus,
          filter,
        );
        suggestion.hidden = !isVisible;
        visibleCount += Number(isVisible);
      });

      branch.hidden = visibleCount === 0;
      if (visibleCount && (filter === 'open' || filter === 'resolved')) {
        branch.open = true;
      }
    });
  };

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      applyFilter(button.dataset.historyFilter);
    });
  });

  applyFilter('active');
});
