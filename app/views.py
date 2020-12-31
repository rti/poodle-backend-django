from rest_framework import viewsets, mixins  # , permissions

from .serializers import QuerySerializer
from .models import Query


class QueryViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

#    def get_permissions(self):
#        if self.action == 'retrieve':
#            permission_classes = [permissions.AllowAny]
#        elif self.action == 'list':
#            permission_classes = [permissions.AllowAny]
#        else:
#            permission_classes = [permissions.IsAuthenticated]
#
#        return [permission() for permission in permission_classes]
