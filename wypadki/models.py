from django.db import models


class Lokomotywa(models.Model):
    nazwa = models.CharField(
        max_length=100,
        help_text="Seria/oznaczenie, np. 'Pt47', 'EU07'"
    )
    opis = models.TextField(
        blank=True,
        help_text="Krótka charakterystyka pojazdu"
    )
    zdjecie = models.ImageField(
        upload_to='lokomotywy/',
        blank=True,
        null=True,
        help_text="Ilustracja z boku"
    )
    zrodlo_zdjecia = models.CharField(
        max_length=300,
        blank=True,
        help_text="Autor / licencja zdjęcia (np. 'Wikimedia Commons, CC BY-SA 4.0')"
    )

    class Meta:
        verbose_name = "Lokomotywa"
        verbose_name_plural = "Lokomotywy"
        ordering = ['nazwa']

    def __str__(self):
        return self.nazwa


class Zdarzenie(models.Model):
    tytul = models.CharField(
        max_length=200,
        help_text="Nazwa zdarzenia, np. 'Katastrofa pod Otłoczynem'"
    )
    data = models.DateField(
        help_text="Data wypadku"
    )
    miejscowosc = models.CharField(
        max_length=150,
        help_text="Miejsce zdarzenia"
    )
    szerokosc = models.FloatField(
        help_text="Szerokość geograficzna (np. 52.9341) — pinezka na mapie"
    )
    dlugosc = models.FloatField(
        help_text="Długość geograficzna (np. 18.7150) — pinezka na mapie"
    )
    linia_kolejowa = models.CharField(
        max_length=100,
        blank=True,
        help_text="Numer/nazwa linii kolejowej, np. 'Linia 18'"
    )
    opis = models.TextField(
        help_text="Przebieg zdarzenia"
    )
    przyczyna = models.TextField(
        blank=True,
        help_text="Ustalona przyczyna (jeśli znana)"
    )
    liczba_ofiar = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Liczba ofiar śmiertelnych (jeśli znana). Zostaw puste, jeśli brak danych."
    )
    lokomotywa = models.ForeignKey(
        Lokomotywa,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='zdarzenia',
        help_text="Tabor zaangażowany w zdarzenie"
    )

    class Meta:
        verbose_name = "Zdarzenie"
        verbose_name_plural = "Zdarzenia"
        ordering = ['-data']

    def __str__(self):
        return f"{self.tytul} ({self.data.year})"


class Material(models.Model):
    class Typ(models.TextChoices):
        FILM = 'film', 'Film (YouTube)'
        PODCAST = 'podcast', 'Podcast'
        REPORTAZ = 'reportaz', 'Reportaż'
        ARTYKUL = 'artykul', 'Artykuł prasowy'
        ZDJECIE = 'zdjecie', 'Zdjęcie / grafika'

    zdarzenie = models.ForeignKey(
        Zdarzenie,
        on_delete=models.CASCADE,
        related_name='materialy',
        help_text="Zdarzenie, do którego należy materiał"
    )
    typ = models.CharField(
        max_length=20,
        choices=Typ.choices,
        default=Typ.ARTYKUL,
        help_text="Rodzaj materiału"
    )
    tytul = models.CharField(
        max_length=300,
        help_text="Nazwa materiału"
    )
    url = models.URLField(
        max_length=500,
        help_text="Pełny link do materiału lub ID filmu YouTube (np. 'dQw4w9WgXcQ')"
    )
    zrodlo = models.CharField(
        max_length=200,
        blank=True,
        help_text="Pochodzenie materiału (np. 'Polskie Radio', 'Archiwum TVP')"
    )

    class Meta:
        verbose_name = "Materiał"
        verbose_name_plural = "Materiały"
        ordering = ['typ', 'tytul']

    def __str__(self):
        return f"[{self.get_typ_display()}] {self.tytul}"
