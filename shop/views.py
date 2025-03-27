from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import joblib

from shop.forms import CommentForm
from .models import Product, Payment, User,Comments
from django.contrib import messages


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
        'purchased_products': purchased_products
    })

def comment_add(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    


def product_comments(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        redirect('login')
    user = User.objects.get(id=user_id)
    product = get_object_or_404(Product, id=product_id)
    comments = Comments.objects.filter(product=product)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = user
            bow_model = joblib.load("bow_model.plk")
            tfidf_model = joblib.load("tfidf_model.plk")

            new_comment = [comment.content]

            # Prédiction
            # pred_bow = bow_model.predict(new_comment)[0]
            comment.type = tfidf_model.predict(new_comment)[0]  
            comment.save()
            return redirect('comments', product_id=product.id)  # Recharge la page après l'ajout
    else:
        form = CommentForm()

    return render(request, 'shop/comment_form.html', {
        'product': product,
        'form': form,
        'comments': comments
    })




def payment_view(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    user = User.objects.get(id=user_id)

    payement = Payment()
    payement.user = user
    payement.product = product
    payement.save()

    return redirect('product_list')