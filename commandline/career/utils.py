from django.core.validators import RegexValidator


PhoneValidator = RegexValidator(
    regex=r'^(0|\+98|0098)9[0-9]{9}$',
    message='Phone number format is not valid.',
    code='invalid_phone_number'
)
