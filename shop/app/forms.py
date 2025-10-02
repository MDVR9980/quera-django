from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Product


# ModelForm for Product with custom validations
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "price", "stock"]

    # Validate price to not exceed 1000
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price > 1000:
            raise ValidationError("Product is too expensive")
        return price

    # Validate description length to be more than 20 characters
    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) <= 20:
            raise ValidationError("Product must have a good description")
        return description
