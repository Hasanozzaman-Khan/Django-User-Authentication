from django.shortcuts import render, redirect
# from django.shortcuts import get_object_or_404
from . import models
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import FormView,View, ListView,TemplateView
# from django.views.generic import DetailView
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm

from django.core.mail import EmailMessage
from django.contrib import messages
# from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from account.tokens import token_generator

from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def send_active_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    email_body = render_to_string('account/activate.html',{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    })
    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_USER,
        to=[user.email],
    )
    email.send(fail_silently=False)


class HomeView(ListView):
    model = models.Home
    template_name = 'account/home.html'

class RegisterView(FormView):
    template_name = 'account/register.html'
    form_class = SignUpForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            send_active_email(user, request)

            messages.success(request, f'A user verification link has been send to confirm your registration.')
            return render(request, 'account/register.html')

        return render(request, self.template_name, {'form': form})

        def get(self, *args, **kwargs):
            if self.request.user.is_authenticated:
                return redirect('login')
            return super(RegisterView, self).get(*args, **kwargs)


class VerificationView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = models.CustomRegisterModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.is_email_verified = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been activated.'))
            return redirect('account:home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('account:login')



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

# class ProfileView(LoginRequiredMixin, DetailView):
#     model = models.CustomRegisterModel
#     template_name = 'account/profile.html'
#     def get_context_data(self, **kwargs):
#         context = super(ProfileView, self).get_context_data(**kwargs)
#         return context
    # def get_object(self): #if first name is unique
    #     return get_object_or_404(models.ProfileModel, user__first_name=self.kwargs['first_name'])


@login_required
def profileView(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form =ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profilemodel)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile has been updated.')
            return redirect('account:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form =ProfileUpdateForm(instance=request.user.profilemodel)

    context = {'u_form':u_form, 'p_form':p_form}
    template_name = 'account/profile_update.html'
    return render(request, template_name, context)


# from django.views.generic import UpdateView
#
# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = models.ProfileModel #CustomRegisterModel #ProfileModel
#     form_class = ProfileUpdateForm
#     template_name = "account/profile_update.html"

    # def get_object(self, *args, **kwargs):
    #     user = get_object_or_404(models.CustomRegisterModel, pk=self.kwargs['pk']) #pk=self.kwargs['pk']
    #     print(user.profilemodel)
    #     print(user.id)
    #     return user.profilemodel
    #
    # def get_success_url(self, *args, **kwargs):
    #     user = get_object_or_404(models.CustomRegisterModel, pk=self.kwargs['pk'])
    #     return reverse_lazy('account:profile', args = (self.user.id,)) #args = (self.object.id,)

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
    #     return context
    # def get_queryset(self):
    #     base_qs = super(ProfileUpdateView, self).get_queryset()
    #     return base_qs.filter(email=self.request.user.email)
