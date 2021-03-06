""" Views of list app. Visitors can view and create lists and listitems. """
from django.shortcuts import render, redirect
from .models import List
from .forms import ItemForm, ExistingListItemForm, NewListForm
from django.contrib.auth import get_user_model
User = get_user_model()

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, pk):
    list_ = List.objects.get(id=pk)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form, })

def share_list(request, pk):
    list_ = List.objects.get(id=pk)
    if request.method == 'POST':
        email = request.POST['email']
        list_.share(email)
    return redirect(list_)

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated():
            list_.owner = request.user
        list_.save()
        form.instance.list = list_
        form.save()
        return redirect(list_)
    else:
        return render(request, 'home.html', {'form': form})

def new_list2(request):
    NewListForm(data=request.POST)

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})
