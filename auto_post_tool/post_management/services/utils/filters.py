from django.db.models import Q


class PostFiltersUtils:
    def __init__(self):
        pass

    @staticmethod
    def handle_post_filter_dict(key, value):
        if key == "post_type":
            filter = Q()
            post_types = value if isinstance(value, list) else value.split(",")
            for post_type in post_types:
                filter = filter | Q(post_type__icontains=post_type)
            return filter

    @staticmethod
    def filters_translate(filters, handle_function):
        filters_translate = Q()
        for key, value in filters.__dict__.items():
            if value is not None:
                filters_translate = filters_translate & handle_function(key, value)
        return filters_translate
