from rest_framework import mixins, generics
from main.serializers import StatusReportSerializer
from main.models import StatusReport


class StatusCollection(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):
    
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class StatusMember(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = StatusReport.objects.all()
    serializer_class = StatusReportSerializer
    permission_classes = (permissions.IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
