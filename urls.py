from django.urls import include, path

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    path('v1/', include('api.urls', namespace='api')),
]
