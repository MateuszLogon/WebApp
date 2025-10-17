from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required
from .models import Item
from .forms import ItemForm

@otp_required
@login_required
def item_list(request):
    """Display and add items."""
    items = Item.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST' and 'name' in request.POST:
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect('shop:item_list')
    else:
        form = ItemForm()

    return render(request, 'shop/item_list.html', {'items': items, 'form': form})


@otp_required
@login_required
def delete_item(request, item_id):
    """Delete selected item (only if owned by current user)."""
    item = get_object_or_404(Item, id=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('shop:item_list')
    return redirect('shop:item_list')
