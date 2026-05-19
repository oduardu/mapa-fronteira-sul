from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Local
from .polygon import ponto_dentro_fronteira


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'autocomplete': 'username',
            'autofocus': True,
            'placeholder': 'Nome de usuário',
        }),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': 'Senha',
        }),
    )


class LocalForm(forms.ModelForm):
    class Meta:
        model = Local
        fields = [
            'nome', 'categoria', 'lat', 'lng',
            'cidade', 'uf', 'resumo', 'descricao',
            'endereco', 'periodo', 'ativo',
        ]
        widgets = {
            'resumo': forms.Textarea(attrs={'rows': 3}),
            'descricao': forms.Textarea(attrs={'rows': 5}),
            'lat': forms.NumberInput(attrs={'step': 'any', 'id': 'id_lat'}),
            'lng': forms.NumberInput(attrs={'step': 'any', 'id': 'id_lng'}),
        }

    def clean(self):
        cleaned = super().clean()
        lat = cleaned.get('lat')
        lng = cleaned.get('lng')
        if lat is not None and lng is not None:
            if not ponto_dentro_fronteira(lat, lng):
                raise forms.ValidationError(
                    'As coordenadas estão fora da região da Fronteira Sul. '
                    'Selecione um ponto dentro da área delimitada no mapa.'
                )
        return cleaned
