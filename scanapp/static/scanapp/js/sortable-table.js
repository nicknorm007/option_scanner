// sortable-table.js

function parseValue(value, type) {
  if (type === 'number') {
    const n = parseFloat(value.replace(/[^0-9.-]+/g, "")); // strip $ and other chars
    return isNaN(n) ? -Infinity : n;
  }
  return value.toString().toLowerCase();
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('th[data-sort]').forEach((th) => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
      const table = th.closest('table');
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.querySelectorAll('tr'));
      const index = Array.from(th.parentNode.children).indexOf(th);
      const sortType = th.getAttribute('data-sort');
      const currentAsc = th.classList.contains('asc');

      // Clear sort classes
      table.querySelectorAll('th').forEach(th => th.classList.remove('asc', 'desc'));

      // Toggle sort direction
      th.classList.toggle('asc', !currentAsc);
      th.classList.toggle('desc', currentAsc);

      rows.sort((a, b) => {
        const aText = a.children[index].textContent.trim();
        const bText = b.children[index].textContent.trim();

        const aVal = parseValue(aText, sortType);
        const bVal = parseValue(bText, sortType);

        if (aVal < bVal) return currentAsc ? 1 : -1;
        if (aVal > bVal) return currentAsc ? -1 : 1;
        return 0;
      });

      rows.forEach(row => tbody.appendChild(row));
    });
  });
});
