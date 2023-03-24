from rest_framework import mixins, viewsets


class CreateOrList(mixins.CreateModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    pass
