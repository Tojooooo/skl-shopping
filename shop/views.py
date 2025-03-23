from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Payment, User
from django.forms import ModelForm
from django.contrib import messages


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['comment']


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('product_list')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, 'shop/login.html')


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create(username=username, password=password1)
            request.session['user_id'] = user.id
            return redirect('product_list')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'shop/register.html')


def product_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    products = Product.objects.all()
    user = User.objects.get(id=user_id)
    user_payments = Payment.objects.filter(user=user)
    purchased_products = [payment.product for payment in user_payments]

    return render(request, 'shop/home.html', {
        'products': products,
        'purchased_products': purchased_products,
        'user_payments': user_payments
    })


def payment_view(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.product = product
            payment.user = user
            payment.save()
            return redirect('product_list')
    else:
        form = PaymentForm()

    return render(request, 'shop/order_form.html', {
        'product': product,
        'form': form
    })