from django.urls import path

from gateway.api import views

app_name = "api"

urlpatterns = [
    path("gateways/", views.GatewayCreateView.as_view(), name="gateway"),
]
