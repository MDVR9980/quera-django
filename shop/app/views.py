from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Order


# View to calculate the total price of an order
def checkout(request, order_pk):
    # Get order by primary key, return 404 if not found
    order = get_object_or_404(Order, pk=order_pk)

    # Calculate total price from all order items
    total = sum(
        item.product.price * item.quantity for item in order.orderitem_set.all()
    )

    # Round total to 2 decimal places
    total = round(total, 2)

    # Return JSON response with total price as a string
    return JsonResponse({"total_price": f"{total:.2f}"})
