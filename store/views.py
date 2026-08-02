from django.shortcuts import render, redirect
from .models import Customer


def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            Customer.objects.get(
                username=username,
                password=password
            )
            return redirect("home")

        except Customer.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid Username or Password"
            })

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            Customer.objects.create(
                full_name=full_name,
                email=email,
                username=username,
                password=password
            )
            return redirect("login")

    return render(request, "signup.html")


def logout(request):
    return redirect("login")


def cart(request):
    cart_items = request.session.get("cart", [])
    total = sum(item["price"] for item in cart_items)

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })


def add_to_cart(request, product, price):
    cart = request.session.get("cart", [])

    cart.append({
        "product": product,
        "price": int(price)
    })

    request.session["cart"] = cart

    return redirect("cart")


def checkout(request):
    if request.method == "POST":
        # Order placed, clear cart
        request.session["cart"] = []
        return redirect("order_success")

    return render(request, "checkout.html")


def order_success(request):
    return render(request, "order_success.html")