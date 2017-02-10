from rest_framework import serializers
from .models import StatusReport


class StatusReportSerializer(serializers.Serializer):

    id = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()
    when = serializers.DateTimeField()
    status = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return StatusReport(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.when = validated_data.get('when', instance.when)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
