from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import City


@require_GET
def cities_by_state(request):
    state_id = request.GET.get('state_id')
    if not state_id:
        return JsonResponse({'cities': []})
    cities = list(City.objects.filter(state_id=state_id).values('id', 'name').order_by('name'))
    return JsonResponse({'cities': cities})
