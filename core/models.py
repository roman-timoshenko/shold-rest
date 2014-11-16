from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils import find_circle_intersections


class Region(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('region_name'), blank=False, db_index=True)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta():
        verbose_name = _('region')
        verbose_name_plural = _('regions')


class Village(models.Model):
    id = models.IntegerField(verbose_name=_('village_id'), primary_key=True, unique=True)
    name = models.CharField(max_length=64, verbose_name=_('village_name'), blank=False, db_index=True)
    region = models.ForeignKey(Region, verbose_name=_('village_region'), blank=False, null=True, default=None)
    x = models.FloatField(verbose_name=_('village_coordinate_x'))
    y = models.FloatField(verbose_name=_('village_coordinate_y'))

    def __unicode__(self):
        return u'[%09d] %s' % (self.id, self.name)

    class Meta:
        verbose_name = _('village')
        verbose_name_plural = _('villages')
        unique_together = (('x', 'y'),)
        index_together = (('x', 'y'),)


ARMY_TYPES_CHOICES = (
    ('full', _('Army full')),
    ('arch', _('Archers')),
    ('capt', _('Captain')),
)

class ArmyRequest(models.Model):
    user = models.ForeignKey(User)
    village = models.ForeignKey(Village)
    type = models.CharField(max_length=4,choices=ARMY_TYPES_CHOICES,default=ARMY_TYPES_CHOICES[0][0])

    def __unicode__(self):
        return u'%s [%s] - %s' % (self.user.username, self.village.id, self.type)



    class Meta:
        unique_together = ['user', 'village', 'type']



def calculate_initial_villages(village_a_name, village_b_name, village_c_name, village_a_id, village_b_id, village_c_id,
                               ab, bc, ca):
    """
    Calculates three initial villages by distances between them. Names and IDs are used to build Village objects.

    Village A becomes the origin.
    Village B is set on X-axis 'ab' units away.
    Village C position is calculated using two circles intersection method.
    Position for village C below or above X-axis is chosen randomly between two circle intersection points.

          c
     ca /   \ bc
      /      \
    a ------- b


    :type village_a_name: str
    :param village_a_name: name of the first village
    :type village_b_name: str
    :param village_b_name: name of the second village
    :type village_c_name: str
    :param village_c_name: name of the third village
    :type village_a_id: int
    :param village_a_id: id of the first village
    :type village_b_id: int
    :param village_b_id: id of the second village
    :type village_c_id: int
    :param village_c_id: id of the third village
    :type ab: float
    :param ab: distance from the first village to the second one
    :type bc: float
    :param bc: distance from the second village to the third one
    :type ca: float
    :param ca: distance from the third village to the first one
    :rtype: (Village, Village, Village)
    :return: a tuple of three new Village instances with calculated coordinates
    """
    intersections = find_circle_intersections(0, 0, ca, ab, 0, bc)
    intersection = intersections[0]
    village_a = Village(id=village_a_id, name=village_a_name, x=0, y=0)
    village_b = Village(id=village_b_id, name=village_b_name, x=ab, y=0)
    village_c = Village(id=village_c_id, name=village_c_name, x=intersection[0], y=intersection[1])
    return village_a, village_b, village_c
