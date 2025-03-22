# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Payment
from .forms import PaymentForm


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})


def payment_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = Order(
                product=product,
                customer_name=form.cleaned_data['name'],
                customer_email=form.cleaned_data['email']
            )
            order.save()
            # Process payment (you'd add payment gateway integration here)
            order.paid = True
            order.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()

    return render(request, 'shope/order_form.html', {
        'product': product,
        'form': form
    })