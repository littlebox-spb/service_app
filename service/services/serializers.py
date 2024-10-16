from .models import Subscription
from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.company_name")
    email = serializers.EmailField(source="client.user.email")

    class Meta:
        model = Subscription
        fields = (
            "id",
            "plan_id",
            "client_name",
            "email",
        )
