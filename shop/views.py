from pathlib import Path
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Payment, User
from django.forms import ModelForm
from django.contrib import messages
from .Classifier import Classifier
import pandas as pd
from .training.word2vec import train_word2vec_model
from sklearn.model_selection import train_test_split


base_dir = Path(__file__).resolve().parent


class CommentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['comment']

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
            request.session['username'] = user.username  # Store username in session
            return redirect('product_list')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password')
    return render(request, 'shop/login.html')


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['username']
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create(username=username, password=password1)
                request.session['user_id'] = user.id
                request.session['username'] = user.username
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
    user_payments = Payment.objects.filter(user=user).order_by('-order_date')

    # Vérifier quels produits ont été achetés (pas seulement commentés)
    purchased_products = set(
        Payment.objects.filter(user=user, is_purchase=True).values_list('product', flat=True)
    )

    # Group payments by product
    product_payments = {}
    for payment in user_payments:
        if payment.product not in product_payments:
            product_payments[payment.product] = []
        product_payments[payment.product].append(payment)

    return render(request, 'shop/home.html', {
        'products': products,
        'product_payments': product_payments,
        'user_payments': user_payments,
        'purchased_products': purchased_products
    })


def payment_view(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    user = User.objects.get(id=user_id)

    # Raha efa nividy
    has_purchased = Payment.objects.filter(user=user, product=product, is_purchase=True).exists()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.product = product
            payment.user = user
            payment.is_purchase = True  # C'est un achat

            # Analyser 
            if payment.comment:
                analyzer = Classifier()
                payment.sentiment = analyzer.analyze_sentiment(text=payment.comment, method="word2vec")

            payment.save()
            messages.success(request, f"Vous avez acheté {product.name} avec succès!")
            return redirect('product_list')
    else:
        if has_purchased:
            return redirect('add_comment', product_id=product_id)
        form = PaymentForm()

    return render(request, 'shop/order_form.html', {
        'product': product,
        'form': form,
        'is_purchase': True
    })


# Nouvelle vue pour ajouter un commentaire sur un produit déjà acheté
def add_comment_view(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)
    user = User.objects.get(id=user_id)

    if not Payment.objects.filter(user=user, product=product, is_purchase=True).exists():
        messages.error(request, "Vous devez d'abord acheter ce produit avant de pouvoir commenter.")
        return redirect('payment', product_id=product_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.product = product
            payment.user = user
            payment.is_purchase = False

            # Analyser le sentiment du commentaire
            analyzer = Classifier()
            payment.sentiment = analyzer.analyze_sentiment(text=payment.comment, method="word2vec")

            payment.save()
            messages.success(request, "Votre commentaire a été ajouté avec succès!")
            return redirect('product_list')
    else:
        form = CommentForm()

    return render(request, 'shop/comment_form.html', {
        'product': product,
        'form': form,
        'is_purchase': False
    })
    
def add_new_data(request):
    user_id = request.session.get('user_id')
    base_dir = Path(__file__).resolve().parent

    if not user_id:
        return redirect('login')
        
    if request.method == 'POST':
        comment = request.POST.get('comment')
        label = request.POST.get('label')
        
        csv_file_path = base_dir / 'training' / 'data' / 'avis.csv'
        
        try:
            with open(csv_file_path, 'a', encoding='utf-8') as f:
                f.write(f'\n{comment};{label}\n')
            
            if 'retrain' in request.POST:
                df = pd.read_csv(csv_file_path, delimiter=';')
                X = df['phrase'].values
                y = df['label'].values
                
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                
                train_word2vec_model(X_train, X_test, y_train, y_test)
                
                messages.success(request, "Vita ny entrainement")
            else:
                messages.success(request, "Tafiditra ny data")
            
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout de données: {str(e)}")
        
    
    return render(request, 'shop/add_data.html')