import json
from decimal import Decimal

from django.test import TestCase, Client
from django.shortcuts import reverse

from app.forms import ProductForm
from app.models import Product, Order, Category, OrderItem


class TestSample(TestCase):
    def setUp(self):
        self.client = Client()
        order = Order.objects.create(address="torgozabad", email="fashabori@email.com")
        category = Category.objects.create(name="bomb")
        product = Product.objects.create(category=category, name="atomic_bomb", price=Decimal("1611.29"), stock=5)
        OrderItem.objects.create(order=order, product=product)

    def test_available_model_manager_default_manager(self):
        self.assertEqual(Product._meta.default_manager, Product.objects)

    def test_correct_model_form(self):
        data = {
            "category": 1,
            "name": "pc",
            "description": "dfkjas;ldfkjas;ldfjkc",
            "price": "999.00",
            "stock": 2,
        }
        form = ProductForm(data)
        self.assertTrue(form.is_valid())

    def test_checkout(self):
        expected = {"total_price": "1611.290000"}
        res = self.client.get(reverse('checkout', args=(1,)))
        data = json.loads(res.content.decode())
        self.assertEqual(Decimal(expected["total_price"]), Decimal(data['total_price']))
