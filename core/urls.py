from django.conf.urls import url, patterns

from core.views import VillageList, DistanceView, UserList, VillageDetail, UserDetail, ApiRoot, RegionList, RegionDetail, \
    InitVillagesView, AddVillageView, FindVillagesInRadius, VillageCount, FindVillagesByNameOrId


urlpatterns = patterns('core.views',
   url(r'^$', ApiRoot.as_view(), name='api-root'),
   url(r'^users/$', UserList.as_view(), name='user-list'),
   url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
   url(r'^villages/$', VillageList.as_view(), name='village-list'),
   url(r'^villages/filter/$', FindVillagesByNameOrId.as_view(), name='village-list-filtered'),
   url(r'^villages/count/$', VillageCount.as_view(), name='village-list-count'),
   url(r'^villages/(?P<pk>\d+)/$', VillageDetail.as_view(), name='village-detail'),
   url(r'^regions/$', RegionList.as_view(), name='region-list'),
   url(r'^regions/(?P<pk>\d+)/$', RegionDetail.as_view(), name='region-detail'),
   url(r'distance/(?P<a>\d+)/(?P<b>\d+)/$', DistanceView.as_view(), name='get-distance'),
   url(r'villages/init/$', InitVillagesView.as_view(), name='init-villages'),
   url(r'villages/add/$', AddVillageView.as_view(), name='add-village'),
   url(r'villages/find/radius/$', FindVillagesInRadius.as_view(), name='find-villages-in-radius'),
)
