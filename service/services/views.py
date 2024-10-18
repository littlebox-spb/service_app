from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Subscription
from .serializers import SubscriptionSerializer
from clients.models import Client
from django.db.models import Prefetch, F, Sum


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        "plan",
        Prefetch(
            "client",
            queryset=Client.objects.all()
            .select_related("user")
            .only("company_name", "user__email"),
        ),
    )

    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {"result": response.data}
        response_data["total_amount"] = queryset.aggregate(total=Sum("price")).get(
            "total"
        )
        response.data = response_data
        return response
