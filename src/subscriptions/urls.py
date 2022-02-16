from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    CreateCheckoutSession,
    CustomerPortal,
    GetPlans,
    Webhook
)

urlpatterns = [
    path('create-session/', CreateCheckoutSession.as_view()),
    path('get-plans/', GetPlans.as_view()),
    path('create-customer-portal/', CustomerPortal.as_view()),
    path('webhook/', Webhook.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
