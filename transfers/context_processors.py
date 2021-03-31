from .models import CategoryTransfer


def category(request):
    return {'category_list': CategoryTransfer.objects.all()}
