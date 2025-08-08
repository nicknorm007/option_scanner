# scanapp/views.py
from django.shortcuts import render
from django.contrib import messages
from .forms import OptionScanForm
from .option_scan import scan_options
from datetime import datetime, timedelta, date

def scan_view(request):
    results = []
    total_premium = 0.0
    total_collateral = 0.0

    if request.method == "POST":
        form = OptionScanForm(request.POST)
        if form.is_valid():
            symbols = form.cleaned_data["symbols"]  # list, e.g. ["HOOD","AMD"]
            query_date = form.cleaned_data["query_date"].strftime("%Y-%m-%d")
            expiration_date = form.cleaned_data["expiration_date"].strftime("%Y-%m-%d")
            delta_target = form.cleaned_data["delta_target"]
            option_type = form.cleaned_data["option_type"]

            try:
                results, total_premium, total_collateral = scan_options(
                    symbols=symbols,
                    query_date=query_date,
                    expiration_date=expiration_date,
                    delta_target=delta_target,
                    option_type=option_type,  # api_key omitted -> pulled from env in option_scan.py
                )

                # Highlight earnings within next 30 days
                today = date.today()
                for row in results:
                    earnings_str = row.get('EarningsDate')
                    row['IsUpcomingEarnings'] = False

                    if earnings_str:
                        try:
                            earnings_date = datetime.strptime(earnings_str, "%Y-%m-%d").date()
                            if today <= earnings_date <= today + timedelta(days=30):
                                row['IsUpcomingEarnings'] = True
                        except ValueError:
                            pass

            except ValueError as ve:
                # likely missing API key; show a friendly message
                messages.error(request, str(ve))
            except Exception as e:
                messages.error(request, f"Unexpected error: {e}")
        else:
            messages.error(request, "Please fix the errors in the form and try again.")
    else:
        form = OptionScanForm()

    return render(
        request,
        "scanapp/scan.html",
        {
            "form": form,
            "results": results,
            "total_premium": total_premium,
            "total_collateral": total_collateral,
        },
    )
