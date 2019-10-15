from django import forms


class ReservationForm(forms.Form):
    name = forms.CharField(label='Your full name', max_length=254)
    email = forms.EmailField(label='Email address', max_length=256)
    valid_from = forms.DateTimeField(label='From')
    valid_until = forms.DateTimeField(label='To')
    reservation = forms.BooleanField(label='Parking reservation')

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        valid_from = cleaned_data.get('valid_from')
        valid_until = cleaned_data.get('valid_until')
        reservation = cleaned_data.get('reservation')
        if not name and not email and not valid_from and not valid_until:
            raise forms.ValidationError('Please insert required data!')

