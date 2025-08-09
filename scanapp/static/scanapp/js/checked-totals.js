document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('.row-checkbox');
  const checkedTotalsRow = document.getElementById('checked-totals-row');
  const checkedTotalPremium = document.getElementById('checked-total-premium');
  const checkedTotalCollateral = document.getElementById('checked-total-collateral');

  function updateCheckedTotals() {
    let totalPremium = 0;
    let totalCollateral = 0;
    let anyChecked = false;

    checkboxes.forEach((cb) => {
      if (cb.checked) {
        anyChecked = true;
        const row = cb.closest('tr');
        const premiumText = row.children[8].textContent.replace(/[^0-9.-]+/g, "");
        const collateralText = row.children[9].textContent.replace(/[^0-9.-]+/g, "");

        totalPremium += parseFloat(premiumText) || 0;
        totalCollateral += parseFloat(collateralText) || 0;
      }
    });

    if (anyChecked) {
      checkedTotalsRow.style.display = '';
      checkedTotalPremium.textContent = `$${totalPremium.toFixed(2)}`;
      checkedTotalCollateral.textContent = `$${totalCollateral.toFixed(2)}`;
    } else {
      checkedTotalsRow.style.display = 'none';
    }
  }

  checkboxes.forEach(cb => cb.addEventListener('change', updateCheckedTotals));
});
