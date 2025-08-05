from django import forms

SYMBOL_CHOICES = [
    ('HOOD', 'HOOD'), ('IREN', 'IREN'), ('SOFI', 'SOFI'), ('CELH', 'CELH'),
    ('AFRM', 'AFRM'), ('PLTR', 'PLTR'), ('AMD', 'AMD'), ('CHWY', 'CHWY'),
    ('HIMS', 'HIMS'), ('IBIT', 'IBIT'), ('BULL', 'BULL'), ('RDDT', 'RDDT'),
    ('SBUX', 'SBUX'), ('RKLB', 'RKLB'), ('UBER', 'UBER'), ('AMZN', 'AMZN')
]

class OptionScanForm(forms.Form):
    symbols = forms.MultipleChoiceField(
        choices=SYMBOL_CHOICES,
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
    
