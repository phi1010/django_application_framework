from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import auth_login, LoginView
from graphene_django.views import GraphQLView

urlpatterns = [
    path('', include('web_homepage.urls')),
    #path('cards/', include('cards.urls')),
    path(
        'accounts/login/',
        LoginView.as_view(
            template_name='admin/login.html',
            extra_context={
                'title': 'Login',
                'site_title': 'Login',
                'site_header': 'Login'}),
        name='login'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('opa-bundles/', include('opa_bundles.urls')),
    path('api/', GraphQLView.as_view(graphiql=True)),
    path("admin/", admin.site.urls),
    path('', include('django_prometheus.urls')),
]

#if settings.DEBUG:
#    import debug_toolbar
#
#    urlpatterns += [
#        path('__debug__/', include(debug_toolbar.urls)),
#    ]

if settings.OIDC:
    urlpatterns += [
        path('oidc/', include('mozilla_django_oidc.urls')),
    ]
