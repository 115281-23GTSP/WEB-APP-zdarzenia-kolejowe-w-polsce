from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Zdarzenie

def mapa_widok(request):
    """Widok renderujący główny szablon mapy z Leafletem."""
    return render(request, 'mapa.html')

def api_zdarzenia(request):
    """Endpoint API zwracający wszystkie zdarzenia wraz z powiązanymi obiektami."""
    zdarzenia = Zdarzenie.objects.select_related('lokomotywa').prefetch_related('materialy').all()
    dane_wyjsciowe = []

    for zdarzenie in zdarzenia:
        lista_materialow = []
        for mat in zdarzenie.materialy.all():
            lista_materialow.append({
                'typ': mat.get_typ_display(),
                'tytul': mat.tytul,
                'url': mat.url,
                'zrodlo': mat.zrodlo
            })

        dane_lokomotywy = None
        if zdarzenie.lokomotywa:
            dane_lokomotywy = {
                'nazwa': zdarzenie.lokomotywa.nazwa,
                'opis': zdarzenie.lokomotywa.opis,
                'zdjecie_url': zdarzenie.lokomotywa.zdjecie.url if zdarzenie.lokomotywa.zdjecie else None,
                'zrodlo_zdjecia': zdarzenie.lokomotywa.zrodlo_zdjecia
            }

        dane_wyjsciowe.append({
            'id': zdarzenie.id,
            'tytul': zdarzenie.tytul,
            'data': zdarzenie.data.strftime('%Y-%m-%d'),
            'miejscowosc': zdarzenie.miejscowosc,
            'szerokosc': zdarzenie.szerokosc,
            'dlugosc': zdarzenie.dlugosc,
            'linia_kolejowa': zdarzenie.linia_kolejowa,
            'opis': zdarzenie.opis,
            'przyczyna': zdarzenie.przyczyna,
            'liczba_ofiar': zdarzenie.liczba_ofiar,
            'lokomotywa': dane_lokomotywy,
            'materialy': lista_materialow
        })

    return JsonResponse(dane_wyjsciowe, safe=False)
