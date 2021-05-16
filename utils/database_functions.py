from django.db.models import Case, When, Value, CharField, Q
from django.db.models.functions import Concat, Cast

from pets.models import Pet


def queryset_for_data_tables(queryset, q_list, order_column_choices, **kwargs):
    draw = int(kwargs.get('draw', None)[0])
    length = int(kwargs.get('length', None)[0])
    start = int(kwargs.get('start', None)[0])
    search_value = kwargs.get('search[value]', None)[0]
    order_column = kwargs.get('order[0][column]', None)[0]
    order = kwargs.get('order[0][dir]', None)[0]

    order_column = order_column_choices[order_column]

    if order == 'desc':
        if isinstance(order_column, str):
            order_column = '-' + order_column
        else:
            order_column = ('-' + col for col in order_column)

    total = queryset.count()

    if search_value:
        queryset = queryset.filter(q_list(search_value))

    count = queryset.count()
    # order
    if isinstance(order_column, str):
        queryset = queryset.order_by(order_column)
    else:
        queryset = queryset.order_by(*order_column)
    queryset = queryset[start:start + length]
    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw': draw
    }


def annotate_age():
    return Concat(
        Case(When(years__gt=0, then=Concat('years', Value(' '),
                                           Case(When(years=1, then=Value('year')),
                                                default=Value('years')))),
             default=Value(''), output_field=CharField()),
        Case(When(years__gt=0, then=Value(' and ')), default=Value('')),
        Case(When(months__gt=0, then=Concat('months', Value(' '),
                                            Case(When(months=1, then=Value('month')),
                                                 default=Value('months')))),
             default=Value(''), output_field=CharField()),
        output_field=CharField())


def query_pets_by_args(**kwargs):
    columns_choices = {
        '0': 'id',
        '1': 'name',
        '2': 'breed__specie__name',
        '3': 'breed__name',
        '4': 'sex',
        '5': ('years', 'months'),
        '6': 'price'
    }

    queryset = Pet.objects.annotate(age_str=annotate_age(),
                                    price_str=Case(When(price__isnull=True, then=Value('For Adoption')),
                                                   default=Cast('price', CharField()), output_field=CharField()))

    def get_q_list(search_value):
        q_list = Q(id__icontains=search_value)
        q_list |= Q(name__icontains=search_value)
        q_list |= Q(breed__specie__name__icontains=search_value)
        q_list |= Q(breed__name__icontains=search_value)
        q_list |= Q(age_str__icontains=search_value)
        q_list |= Q(price_str__icontains=search_value)
        return q_list

    return queryset_for_data_tables(queryset, get_q_list, columns_choices, **kwargs)
