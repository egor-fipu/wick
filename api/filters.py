import django_filters as filters
from django.db.models.expressions import RawSQL

from products.models import Notebook
from users.models import User


class NotebookFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name', lookup_expr='contains'
    )

    class Meta:
        model = Notebook
        fields = ('name',)


class UserFilter(filters.FilterSet):
    first_name = filters.CharFilter(
        field_name='first_name', lookup_expr='contains'
    )
    last_name = filters.CharFilter(
        field_name='last_name', lookup_expr='contains'
    )
    gender = filters.CharFilter(
        field_name='gender', lookup_expr='exact'
    )
    distance = filters.NumberFilter(method='filter_distance')

    def filter_distance(self, queryset, name, value):
        user = self.request.user
        if user.latitude is None:
            return queryset
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(latitude))
               * cos(radians(longitude) - radians(%s)) +
               sin(radians(%s)) * sin(radians(latitude))
              )
              """
        new_queryset = queryset \
            .exclude(latitude=None) \
            .exclude(longitude=None) \
            .annotate(distance=RawSQL(gcd, (user.latitude,
                                            user.longitude,
                                            user.latitude))) \
            .filter(distance__lt=value) \
            .order_by('distance')
        return new_queryset

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender')
