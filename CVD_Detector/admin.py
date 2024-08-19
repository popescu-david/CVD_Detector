from django.contrib import admin
from functools import update_wrapper
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from Users.forms import UserLoginForm,UserPasswordResetForm,UserSetPasswordForm

class MyAdminSite(admin.AdminSite):
    index_title='Cardiotest'
    site_title='Administration'
    site_header='Cardiotest'
    def get_urls(self):
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return super(MyAdminSite,self).admin_view(view, cacheable)(*args, **kwargs)
            
            wrapper.admin_site = self
            return update_wrapper(wrapper, view)
        
        urlpatterns = [
            path("", wrap(self.index), name="index"),
            path('login/', auth_views.LoginView.as_view(template_name='Users/login.html', form_class=UserLoginForm), name='login'),
            path('logout/', auth_views.LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
            path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Users/password_reset/password_reset.html', form_class=UserPasswordResetForm),name='password_reset'),
            path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='Users/password_reset/password_reset_done.html'),name='password_reset_done'),
            path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='Users/password_reset/password_reset_confirm.html', form_class=UserSetPasswordForm),name='password_reset_confirm'),
            path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='Users/password_reset/password_reset_complete.html'),name='password_reset_complete'),
            path("jsi18n/", wrap(self.i18n_javascript, cacheable=True), name="jsi18n"),
        ]

        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
                path(
                    "%s/%s/" % (model._meta.app_label, model._meta.model_name),
                    include(model_admin.urls),
                ),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        if valid_app_labels:
            regex = r"^(?P<app_label>" + "|".join(valid_app_labels) + ")/$"
            urlpatterns += [
                re_path(regex, wrap(self.app_index), name="app_list"),
            ]

        if self.final_catch_all_view:
            urlpatterns.append(re_path(r"(?P<url>.*)$", wrap(self.catch_all_view)))

        return urlpatterns
