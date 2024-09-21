from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'image', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """
        Валидация названия и описания продукта на запрещенные слова
        """
        stop_words = (
            'казино',
            'криптовалюта',
            'крипта',
            'биржа',
            'дешево',
            'бесплатно',
            'обман',
            'полиция',
            'радар'
        )

        data = self.cleaned_data
        name = data['name']
        description = data['description']
        for sw in stop_words:
            if sw in name.lower():
                msg = f'В поле НАЗВАНИЕ ПРОДУКТА используется запрещенное слово: {sw}! Отредактируйте ввод'
                self.add_error("name", msg)
            if sw in description.lower():
                msg = f'В поле ОПИСАНИЕ ПРОДУКТА используется запрещенное слово: {sw}! Отредактируйте ввод'
                self.add_error("name", msg)

        return data

