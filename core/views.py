from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _

from core.models import Village, Region, calculate_initial_villages
from core.serializers import VillageSerializer, RegionSerializer, UserSerializer
from core.utils import get_distance, get_fourth_point


class ApiRoot(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        return Response({
            'users': reverse('user-list', request=request),
            'villages': reverse('village-list', request=request),
            'regions': reverse('region-list', request=request),
            'distance': reverse('get-distance', request=request, kwargs={'a': 1, 'b': 2}),
            'init-villages': reverse('init-villages', request=request),
            'add-village': reverse('add-village', request=request)
        })


class UserList(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)


class VillageList(generics.ListCreateAPIView):
    model = Village
    serializer_class = VillageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class VillageDetail(generics.RetrieveUpdateAPIView):
    model = Village
    serializer_class = VillageSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RegionList(generics.ListCreateAPIView):
    model = Region
    serializer_class = RegionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RegionDetail(generics.RetrieveUpdateAPIView):
    model = Region
    serializer_class = RegionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class DistanceView(generics.SingleObjectAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, a, b):
        first = get_object_or_404(Village, pk=a)
        second = get_object_or_404(Village, pk=b)
        distance = get_distance((first.x, first.y), (second.x, second.y))
        return Response({'a': a, 'b': b, 'distance': distance})


class VillageCount(generics.SingleObjectAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        return Response({'count': Village.objects.all().count()})


# {
# "villages": [
# {
# 			"id": 1,
# 			"name": "First"
# 		},
# 		{
# 			"id": 2,
# 			"name": "Second"
# 		},
# 		{
# 			"id": 3,
# 			"name": "Third"
# 		}
# 	],
# 	"ab": 10,
# 	"bc": 10,
# 	"ca": 10
# }
class InitVillagesView(APIView):
    permission_classes = (permissions.IsAdminUser,)

    def post(self, request, *args, **kwargs):
        villages = request.DATA['villages']
        if len(villages) != 3:
            raise ParseError(detail=_("Exactly three village templates should be passed."))
        try:
            result = calculate_initial_villages(villages[0]['name'], villages[1]['name'], villages[2]['name'],
                                                villages[0]['id'], villages[1]['id'], villages[2]['id'],
                                                request.DATA['ab'], request.DATA['bc'], request.DATA['ca'])
            for village in result:
                village.save()
        except ValueError:
            raise ParseError(detail=_("Three given distances cannot form a triangle."))
        except KeyError:
            raise ParseError(detail=_("Invalid data format."))
        serialized = [VillageSerializer(village).data for village in result]
        return Response(serialized)


#{
# "id": 4,
# "name": "Fourth",
# "distances": [
#   {
#     "id": 1,
#     "distance": 10
#   },
#   {
#     "id": 2,
#     "distance": 10
#   },
#   {
#     "id": 3,
#     "distance": 10
#   }
# ]
# }
class AddVillageView(APIView):
    """
    A separate API call to add village using known distances to other three known villages.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        distances = request.DATA['distances']
        if len(distances) != 3:
            raise ParseError(detail=_("Exactly three distances to existing villages should be passed."))
        try:
            a, b, c = get_object_or_404(Village, pk=distances[0]['id']), \
                      get_object_or_404(Village, pk=distances[1]['id']), \
                      get_object_or_404(Village, pk=distances[2]['id'])
            ad, bd, dc = distances[0]['distance'], distances[1]['distance'], distances[2]['distance']
            dx, dy = get_fourth_point((a.x, a.y), (b.x, b.y), (c.x, c.y), ad, bd, dc)
            d = Village(id=request.DATA['id'], name=request.DATA['name'], region=request.DATA['region'], x=dx, y=dy)
            d.save()
        except KeyError:
            raise ParseError(detail=_("Invalid data format."))
        except ValueError as e:
            print(e)
            raise ParseError(detail=_("Cannot evaluate new village location with given distances."))


class FindVillagesByNameOrId(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        query = request.REQUEST['query']
        villages = Village.objects.filter(Q(id__icontains=query) | Q(name__icontains=query))[:10]
        return Response(VillageSerializer(villages, many=True).data)


class FindVillagesInRadius(APIView):
    """
    Finds all villages in radius from a specified village
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        village_id = request.REQUEST['village_id']
        radius = request.REQUEST['radius']
        request_village = get_object_or_404(Village, pk=village_id)
        radius = float(radius)
        result = list()
        for village in Village.objects.all():
            distance = get_distance((request_village.x, request_village.y), (village.x, village.y))
            if distance < radius:
                result.append(village)
        return Response(VillageSerializer(result, many=True).data)
