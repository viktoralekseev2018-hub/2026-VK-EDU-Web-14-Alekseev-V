from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate(objects_list, request, per_page=10):
    """Возвращает Page. Некорректный номер заменяется первой страницей."""
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(request.GET.get("page", 1))
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    page.pagination_range = list(paginator.get_elided_page_range(
        number=page.number, on_each_side=2, on_ends=1
    ))
    return page
