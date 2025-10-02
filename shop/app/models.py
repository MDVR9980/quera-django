from django.db import models


# Category model to store product categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Custom manager to filter only available products (stock > 0)
class ProductManager(models.Manager):
    def get_queryset(self):
        # Return only products with stock greater than 0
        return super().get_queryset().filter(stock__gt=0)


# Product model to store product details
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Managers
    objects = models.Manager()  # Default manager
    available = ProductManager()  # Custom manager for available products

    def __str__(self):
        return self.name


# Order model to store customer orders
class Order(models.Model):
    address = models.CharField(max_length=250)
    email = models.EmailField()

    def __str__(self):
        return "{}".format(self.id)


# OrderItem model to store items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{}".format(self.id)
