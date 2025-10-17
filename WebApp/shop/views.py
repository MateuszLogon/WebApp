from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item
from .forms import ItemForm
from django_otp.decorators import otp_required

otp_required
def item_list(request):
    """
    Displays the list of items belonging only to the logged-in user.
    Also handles the creation of new items via POST.
    """
    items = Item.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user  # associate with the logged-in user
            item.save()
            return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'shop/item_list.html', {'items': items, 'form': form})
