from django.core.paginator import Paginator


def get_page_numbers(queryset, request, keys_limit):
    paginator = Paginator(queryset, keys_limit)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'paginator': paginator,
        'page_number': page_number,
        'page_obj': page_obj
    }