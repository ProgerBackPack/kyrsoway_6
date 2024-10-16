from django.db import models


class Blog(models.Model):
    """
    Модель блога
    """
    tittle = models.CharField(max_length=50, verbose_name="Заголовок",)
    content_article = models.TextField(verbose_name="Описание",)
    images = models.ImageField(upload_to="media/blog/", verbose_name="Изображение", blank=True, null=True,)
    count_view = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0, editable=False)
    published_date = models.DateField(auto_now_add=True, verbose_name="Дата публикации",)

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"

    def __str__(self):
        return self.tittle