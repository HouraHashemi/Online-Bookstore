
from django.shortcuts import render, redirect
from .models import Book

from django.shortcuts import render
from .forms import BookSearchForm

from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Cart
from .models import CartItem
from .models import Order
from .models import OrderItem
from django.shortcuts import redirect, get_object_or_404


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not hasattr(request.user, 'cart'):
                Cart.objects.create(user=request.user)
            return redirect('book_list_have_access')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


# def book_detail(request, book_id):
#     book = Book.objects.get(id=book_id)
#     return render(request, './templates/book_detail.html', {'book': book})


@login_required
def book_list_have_access(request):
    books = Book.objects.all()

    # Get the cart for the current user
    cart = Cart.objects.get(user=request.user)

    # Get the quantity of each book in the cart
    cart_items = cart.items.all()

    context = {
        'books': books,
        'cart_items': cart_items,
    }

    return render(request, 'book_list_have_access.html', context)



@login_required
def add_to_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        # Get or create the user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if the book is already in the cart
        cart_item, created = cart.items.get_or_create(book=book)
        print("----------------")
        print(cart_item, created)
        print("----------------")
        if not created:
            # If the book is already in the cart, increment the quantity
            cart_item.quantity += 1
            cart_item.save()
    return redirect('book_list_have_access')


@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        # Get the cart item for the specified book and user
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            book = get_object_or_404(Book, id=book_id)
            cart_item, created = cart.items.get_or_create(book=book)
            # If the quantity is greater than 1, decrement the quantity
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                # If the quantity is 1, remove the item from the cart
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    return redirect('book_list_have_access')


@login_required
def view_cart(request):
    cart = request.user.cart
    # Retrieve and pass cart items to the template
    cart_items = cart.items.all()  # Assuming you have an 'items' field in your Cart model
    total_price = 0
    for item in cart_items:
        total_price = total_price + item.book.price

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'view_cart.html', context)


def order_submission(request):
    return render(request, 'order_submission.html')


@login_required
def submit_final_order(request):
    if request.method == 'POST':
        # Process form data and create the order
        # Retrieve the form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        cart = request.user.cart
        cart_items = cart.items.all()

        # Create an order
        total_price = 0
        for item in cart_items:
            total_price = total_price + item.book.price
        order = Order.objects.create(user=request.user, total_price=total_price)
        # Move cart items to the order
        for cart_item in cart_items:
            # Create an OrderItem for each cart item
            order_item = OrderItem.objects.create(
                book=cart_item.book,
                quantity=cart_item.quantity,
                price=cart_item.book.price*cart_item.quantity
            )
            # Associate the OrderItem with the order
            order.items.add(order_item)
        # Empty the cart
        cart.items.clear()
        # Redirect to the view_orders page
        return redirect('view_orders')
    else:
        # Handle GET request if needed
        return redirect('order_submission')  
    

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'view_orders.html', {'orders': orders})


def search_books(request):
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            # Perform book search logic using the search query
            # Redirect or render appropriate response
    else:
        form = BookSearchForm()
    return render(request, 'search.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('book_list')
