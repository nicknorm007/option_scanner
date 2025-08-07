from django import forms

import csv
import os
from django import forms

def load_symbol_choices():
    symbol_choices = []
    csv_path = os.path.join(os.path.dirname(__file__), "symbols.csv")
    try:
        with open(csv_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row.get("symbol")
                if symbol:
                    symbol_choices.append((symbol, symbol))
    except FileNotFoundError:
        print(f"symbols.csv not found at {csv_path}")
    return symbol_choices

class OptionScanForm(forms.Form):
    symbols = forms.MultipleChoiceField(
        choices=load_symbol_choices(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    query_date = forms.DateField(
        label='Query Date',
        initial="2025-08-01",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    expiration_date = forms.DateField(
        label='Expiration Date',
        initial="2025-08-15",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    delta_target = forms.FloatField(
        label='Delta Target',
        initial=-0.20
    )
        
    OPTION_TYPE_CHOICES = [
        ("put", "Put"),
        ("call", "Call"),
    ]
    option_type = forms.ChoiceField(
        choices=OPTION_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial="put",
    )
    
