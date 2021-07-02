from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Contact
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages


def index(request):
    contacts = Contact.objects.order_by('-id').filter(show=True)
    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })


def show_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if not contact.show:
        raise Http404()

    return render(request, 'contacts/show_contact.html', {
        'contact': contact
    })


def search(request):
    search = request.GET.get('search')

    if search is None or not search:
        messages.add_message(request, messages.ERROR, 'The field Search cannot be empty.')
        return redirect('index')

    fields = Concat('name', Value(' '), 'last_name')
    contacts = Contact.objects.annotate(
        complete_name=fields
    ).filter(Q(complete_name__icontains=search) | Q(phone__icontains=search))

    paginator = Paginator(contacts, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    return render(request, 'contacts/search.html', {
        'contacts': contacts
    })
