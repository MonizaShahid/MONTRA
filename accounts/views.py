# Django core imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages

# Authentication and permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Class-based views
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

# Third-party packages
from django_tables2 import SingleTableView

# Local app imports
from .models import Profile, Customer, Vendor
from .forms import (
    CreateUserForm, UserUpdateForm,
    ProfileUpdateForm, CustomerForm,
    VendorForm
)
from .tables import ProfileTable


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = CreateUserForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        # Only update profile fields, not user fields
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user-profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(
        request,
        'accounts/profile_update.html',
        {'p_form': p_form}
    )


class ProfileListView(LoginRequiredMixin, SingleTableView):
    model = Profile
    template_name = 'accounts/stafflist.html'
    context_object_name = 'profiles'
    table_class = ProfileTable
    paginate_by = 10
    table_pagination = False


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    template_name = 'accounts/staffcreate.html'
    fields = ['user', 'role', 'status']

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'accounts/staffupdate.html'
    fields = ['user', 'role', 'status']

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Profile
    template_name = 'accounts/staffdelete.html'

    def get_success_url(self):
        return reverse('profile_list')

    def test_func(self):
        return self.request.user.is_superuser


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'accounts/customer_list.html'
    context_object_name = 'customers'


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'accounts/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'accounts/customer_form.html'
    form_class = CustomerForm
    success_url = reverse_lazy('customer_list')


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'accounts/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from transactions.models import Sale
        context['sales_count'] = Sale.objects.filter(customer=self.object).count()
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Check if customer has any sales
        from transactions.models import Sale
        sales_count = Sale.objects.filter(customer=self.object).count()
        
        if sales_count > 0:
            from django.contrib import messages
            messages.error(
                request,
                f'Cannot delete {self.object.get_full_name()}. '
                f'This customer has {sales_count} sales record(s). '
                f'Please delete or reassign the sales first.'
            )
            return redirect(self.success_url)
        
        return super().delete(request, *args, **kwargs)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
@require_POST
@login_required
def get_customers(request):
    if is_ajax(request) and request.method == 'POST':
        term = request.POST.get('term', '')
        customers = Customer.objects.filter(
            name__icontains=term
        ).values('id', 'name')
        customer_list = list(customers)
        return JsonResponse(customer_list, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'accounts/vendor_list.html'
    context_object_name = 'vendors'
    paginate_by = 10


class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'accounts/vendor_form.html'
    success_url = reverse_lazy('vendor-list')


class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'accounts/vendor_form.html'
    success_url = reverse_lazy('vendor-list')


class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendor
    template_name = 'accounts/vendor_confirm_delete.html'
    success_url = reverse_lazy('vendor-list')
