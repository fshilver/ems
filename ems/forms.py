from django import forms
from .models import Equipment, EquipmentSpec


class EquipmentSpecForm(forms.ModelForm):

    class Meta:
        model = EquipmentSpec
        exclude = ('equipment',)

        labels = {
            'cpu': 'CPU',
            'mem': 'Memory',
            'hdd': 'HDD',
            'nic': '네트워크',
            'grahpic': '그래픽카드',
            'manufacturer': '제조사',
            
        }

        widgets = {
            'cpu': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'mem': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'hdd': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'nic': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'graphic': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

class EquipmentForm(forms.ModelForm):

    # EquipmentSpec
    cpu           = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mem           = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hdd           = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nic           = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    graphic       = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    etc           = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    text          = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # change_date   = forms.DateInput(attrs={'class': 'form-control col-md-7 col-xs-12', 'placeholder': '입력 포맷 예) 2018-10-01'}, format='%Y-%m-%d')
    # change_reason = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # cost          = forms.NumberInput(attrs={'class': 'form-control'})
    # change_user   = forms.Select(attrs={'class': 'form-control'})
    # reference     = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # count         = forms.NumberInput(attrs={'class': 'form-control'})

    class Meta:
        model = Equipment
        fields = '__all__'

        labels = {
            'purchase_request_user': '구입 요청자',
            'serial_number': 'S/N',
            'purchase_date': '구입일자',
            'price': '가격',
        }

        widgets = {
            'purchase_request_user': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'purchase_date': forms.DateInput(
                attrs={
                    'class': 'form-control col-md-7 col-xs-12',
                    'placeholder': '입력 포맷 예) 2018-10-01',
                    },
                format='%Y-%m-%d'
            ),
            'price': forms.NumberInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'current_user': forms.Select(attrs={'class': 'form-control'}),
            'kind': forms.Select(attrs={'class': 'form-control'}),
            'management_number': forms.TextInput(attrs={'class': 'form-control'}),
            'accessibility': forms.Select(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control'}),
            'check_in_duedate': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '입력 포맷 예) 2018-10-01',
                    },
                format='%Y-%m-%d'
            ),
            'buying_shop': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_manager': forms.Select(attrs={'class': 'form-control'}),
            'document': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self):
        eq = super().save(commit=False)
        eq.save()

        cpu = self.cleaned_data.get('cpu', None)
        mem = self.cleaned_data.get('mem', None)
        hdd = self.cleaned_data.get('hdd', None)
        nic = self.cleaned_data.get('nic', None)
        graphic = self.cleaned_data.get('graphic', None)
        etc = self.cleaned_data.get('etc', None)
        text = self.cleaned_data.get('text', None)
        EquipmentSpec.objects.create(equipment=eq, cpu=cpu, mem=mem, hdd=hdd, nic=nic, graphic=graphic, etc=etc, text=text)

        return eq
        