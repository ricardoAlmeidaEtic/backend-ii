from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('event-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful registration
        login(self.request, self.object)
        return response

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('event-list')
        return super().dispatch(request, *args, **kwargs) 