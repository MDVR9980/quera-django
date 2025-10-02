from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def introduce(request):
    text = request.GET.get('text', '')
    return render(request, 'postal_card.html', {'postal_card_text': text})
