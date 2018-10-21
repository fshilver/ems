from django import forms
from .models import Equipment, EquipmentSpec, EquipmentApply


class EquipmentSpecForm(forms.ModelForm):

    class Meta:
        model = EquipmentSpec
        exclude = ('equipment',)

        widgets = {
            'cpu': forms.TextInput(attrs={'class': 'form-control'}),
            'mem': forms.TextInput(attrs={'class': 'form-control'}),
            'hdd': forms.TextInput(attrs={'class': 'form-control'}),
            'nic': forms.TextInput(attrs={'class': 'form-control'}),
            'graphic': forms.TextInput(attrs={'class': 'form-control'}),
            'etc': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'change_date': forms.DateInput(
                attrs={
                    'class': 'form-control col-md-7 col-xs-12',
                    'placeholder': '입력 포맷 예) 2018-10-01',
                    },
                format='%Y-%m-%d'
            ),
            'change_reason' : forms.TextInput(attrs={'class': 'form-control'}),
            'cost'          : forms.NumberInput(attrs={'class': 'form-control'}),
            'change_user'   : forms.Select(attrs={'class': 'form-control'}),
            'reference'     : forms.TextInput(attrs={'class': 'form-control'}),
            'count'         : forms.NumberInput(attrs={'class': 'form-control'}),
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


class EquipmentUpdateForm(forms.ModelForm):

    class Meta:
        model = Equipment
        fields = '__all__'
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
        

class EquipmentApplyForm(forms.ModelForm):

    equipment_list = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = EquipmentApply
        exclude = ('user', 'equipment', 'reject_reason', 'status')
        widgets = {
            'purpose': forms.Textarea(attrs={'class': 'form-control'}),
            'check_in_duedate': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '입력 포맷 (2018-10-01)',
                },
                format='%Y-%m-%d',
            ),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }