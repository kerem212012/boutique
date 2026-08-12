from django import forms

from catalog.models import Category, Product, ProductImage


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name_tr', 'name_en', 'description_tr', 'description_en', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].help_text = 'Boş bırakın — otomatik oluşturulur'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class ProductForm(forms.ModelForm):
    sizes_text = forms.CharField(
        required=False,
        label='Bedenler',
        help_text='Virgülle ayırın: S, M, L, XL',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'S, M, L, XL'}),
    )
    colors_text = forms.CharField(
        required=False,
        label='Renkler',
        help_text='Virgülle ayırın: Beyaz, Siyah',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Beyaz, Siyah'}),
    )

    class Meta:
        model = Product
        fields = (
            'name_tr', 'name_en',
            'description_tr', 'description_en',
            'category', 'price', 'image',
            'is_featured', 'slug',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['slug'].help_text = 'Boş bırakın — otomatik oluşturulur'
        for name, field in self.fields.items():
            if name not in ('is_featured', 'image'):
                field.widget.attrs['class'] = 'form-input'
        if self.instance and self.instance.pk:
            self.fields['sizes_text'].initial = ', '.join(self.instance.sizes or [])
            self.fields['colors_text'].initial = ', '.join(self.instance.colors or [])

    def save(self, commit=True):
        product = super().save(commit=False)
        product.sizes = [
            s.strip() for s in self.cleaned_data.get('sizes_text', '').split(',') if s.strip()
        ]
        product.colors = [
            c.strip() for c in self.cleaned_data.get('colors_text', '').split(',') if c.strip()
        ]
        if commit:
            product.save()
        return product


class ProductImageUploadForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image', 'alt_text', 'sort_order')
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Fotoğraf açıklaması (isteğe bağlı)',
            }),
            'sort_order': forms.NumberInput(attrs={'class': 'form-input', 'value': '0'}),
        }
