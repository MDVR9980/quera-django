from django.db import models

from career.utils import PhoneValidator


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=14, validators=[PhoneValidator])
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
