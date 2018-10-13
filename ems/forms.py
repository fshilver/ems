from django import forms
from .models import Equipment, EquipmentSpec

class EquipmentCreationForm(forms.ModelForm):

    cpu          = forms.CharField(
                        max_length=50,
                        label='CPU',
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
                    )
    mem          = forms.CharField(
                        max_length=50,
                        label='Memory',
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
                    )
    hdd          = forms.CharField(
                        max_length=50,
                        label='HDD',
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
                    )
    nic          = forms.CharField(
                        max_length=50,
                        label='네트워크',
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
                    )
    graphic      = forms.CharField(
                        max_length=50,
                        label='그래픽카드',
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
                    )
    manufacturer = forms.CharField(
                        max_length=50,
                        label='제조사',
                        required=False,
                        widget=forms.TextInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
                    )

    class Meta:
        model = Equipment
        exclude = ('current_user',)

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
                    'placeholder': '2018-10-01',
                    },
                format='%Y-%m-%d'
            ),
            'price': forms.NumberInput(attrs={'class': 'form-control col-md-7 col-xs-12'}),
            'status': forms.Select(attrs={'class': 'form-control col-md-7 col-xs-12'}),
        }

    def save(self):
        eq = super().save(commit=False)
        eq.save()

        cpu = self.cleaned_data.get('cpu', None)
        mem = self.cleaned_data.get('mem', None)
        hdd = self.cleaned_data.get('hdd', None)
        nic = self.cleaned_data.get('nic', None)
        graphic = self.cleaned_data.get('graphic', None)
        manufacturer = self.cleaned_data.get('manufacturer', None)
        EquipmentSpec.objects.create(equipment=eq, cpu=cpu, mem=mem, hdd=hdd, nic=nic, graphic=graphic, manufacturer=manufacturer)

        return eq


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
        