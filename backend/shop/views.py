from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required
from .models import Item
from .forms import ItemForm


@otp_required
@login_required
def item_list(request):
    """
    Widok sklepu (lista rzeczy).
    Dostępny tylko po pełnym zalogowaniu i potwierdzeniu MFA.
    """
    items = Item.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'shop/item_list.html')
