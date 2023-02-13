from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from .models import Object, Requirement
from .serializers import ObjectSerializer, UserSerializer, GroupSerializer, RequirementSerializer


class ObjectChildList(generics.ListAPIView):

    serializer_class = ObjectSerializer

    def get_queryset(self):
        """
        This view should return a list of child objects.
        """
        parent = self.kwargs['pk']
        return Object.objects.filter(parent_id=parent)


class ObjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows objects to be viewed or edited.
    """
    serializer_class = ObjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of child objects.
        """
        parent_id = self.request.query_params.get('parent')
        if parent_id and parent_id.isdigit():
            return Object.objects.filter(parent_id=parent_id)
        elif parent_id:
            return Object.objects.filter(parent_id__isnull=True)
        else:
            return Object.objects.all()


class RequirementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows requirement to be viewed or edited.
    """
    serializer_class = RequirementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of child objects.
        """
        object_id = self.request.query_params.get('object')
        if object_id and object_id.isdigit():
            return Requirement.objects.filter(object_id=object_id)
        else:
            return Requirement.objects.all()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@login_required
def index_view(request):
    objects = Object.objects.all()
    context = {
        'objects': objects,
    }
    return render(request, 'material_management/index.html', context=context)