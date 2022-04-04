from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.utils import timezone
from django.views.generic import ListView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import ImageForm, ApartmentForm
from .models import *
from .permissions import UserHasPermissionMixin


class MainPageView(ListView):
    model = Apartment
    template_name = 'index.html'
    context_object_name ='apartments'
    paginate_by = 2

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            template_name = 'search.html'
        elif filter:
            template_name = 'new.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['apartments'] = Apartment.objects.filter(Q(title__icontains=search)|
                                                             Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=2)
            context['apartments'] = Apartment.objects.filter(created__gte=start_date)
        else:
            context['apartments'] = Apartment.objects.all()
        return context




def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    apartments = Apartment.objects.filter(category_id=slug)
    return render(request, 'category-detail.html', locals())


def apt_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    image = apartment.get_image
    images = apartment.images.exclude(id=image.id)
    return render(request, 'apt-detail.html', locals())

@login_required(login_url='login')
def add_info(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        apt_form = ApartmentForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if apt_form.is_valid() and formset.is_valid():
            apartment = apt_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, apartment=apartment)
            return redirect(apartment.get_absolute_url())
    else:
        apt_form = ApartmentForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-info.html', locals())


def update_info(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.user == apartment.user:
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
        apt_form = ApartmentForm(request.POST or None, instance=apartment)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(apartment=apartment))
        if apt_form.is_valid() and formset.is_valid():
            apartment = apt_form.save()

            for form in formset:
                image = form.save(commit=False)
                image.apartment = apartment
                apartment.save()
            return redirect(apartment.get_absolute_url())
        return render(request, 'update-info.html', locals())
    else:
        return HttpResponse('<h1>403 Forbidden</h1>')



# def delete_info(request, pk):
#     apartment = get_object_or_404(Apartment, pk=pk)
#     if request.method == "POST":
#         apartment.delete()
#         messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
#         return redirect('home')
#     return render(request, 'delete-info.html')



class DeleteRecipeView(UserHasPermissionMixin, DeleteView):
    model = Apartment
    template_name = 'delete-info.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return HttpResponseRedirect(success_url)

