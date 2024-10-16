from django import template

register = template.Library()


@register.filter()
def mymedia(path):
    """
    Фильтр для добавления атрибута src к изображениям из media-папки.
    :param path: Путь к изображению в media-папке.
    :return: Ссылка на изображение с добавленным атрибутом src.
    """
    if path:
        return f"/media/{path}"
    return "#"