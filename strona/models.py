# -*- coding: utf-8 -*-
from django.db import models

class Kategorie(models.Model):
	name = models.CharField('Nazwa Kategorii', max_length=100)
	slug = models.SlugField('Odnosnik', unique=True, max_length=100)
	icon = models.ImageField('Ikonka Kategorii', upload_to='icons', blank=True)

	class Meta:
		verbose_name = "Kategoria"
		verbose_name_plural = "Kategorie"
		db_table = 'h_kategorie'
	def __unicode__(self):
		return self.name

class Artykuly(models.Model):
	title = models.CharField('Tytuł', max_length=255)
	slug = models.SlugField('Odnosnik', max_length=255, unique=True)
	wprowadzenie = models.CharField('Wprowadzenie', max_length=255)
	text = models.TextField(verbose_name='Treść')
	categories = models.ManyToManyField(Kategorie, verbose_name='Kategorie')
	posted_date = models.DateTimeField('Data dodania', auto_now_add=False)
	author = models.CharField(verbose_name='Autor', max_length=255)

	class Meta:
		verbose_name = "Artykuł"
		verbose_name_plural = "Artykuły"
		db_table = 'h_artykuly'

	def __unicode__(self):
		return self.title


class Druzyny(models.Model):
	nazwa = models.CharField('Nazwa Drużyny', max_length=500)
	menu_name = models.CharField('Skrócona nazwa Drużyny', max_length=255)
	data_utworzenia = models.DateTimeField('Data utworzenia')
	gzbiorki = models.CharField('Godzina zbiórek', max_length=15)
	mzbiorki = models.CharField('Miejsce zbiórek', max_length=255)
	dziala = models.CharField('Aktywna', max_length=5)
	add_date = models.DateTimeField('Data dodania', auto_now_add=True)
	druzynowy = models.CharField('Drużynowy', max_length=255)
	slug = models.SlugField('Odnosnik', max_length=255, unique=True)
	opis = models.TextField(verbose_name='Opis')

	class Meta:
		verbose_name = "Drużyna"
		verbose_name_plural = "Drużyny"
		db_table = 'szs_druzyny'

	def __unicode__(self):
		return self.nazwa

	def _get_nazwa_druzyny(self):
		"Zwraca Nazwę Drużyny."
		return '%s' % (self.nazwa)
		nazwa_druzyny = property(_get_nazwa_druzyny)

class Osoby(models.Model):
	dru = models.ForeignKey(Druzyny, verbose_name='OsoDru')
	imie = models.CharField('Imie', max_length=255)
	nazwisko = models.CharField('Nazwisko', max_length=255)
	pesel = models.CharField('PESEL', max_length=11)
	telefon = models.CharField('Telefon', max_length=9, blank=True)
	m_urodzenia = models.CharField('Miejsce Urodzenia', max_length=255, blank=True)
	email = models.CharField('Adres Email', max_length=255, blank=True)
	add_date = models.DateTimeField('Data dodania', auto_now_add=True)
	aktywny = models.CharField('Aktywna', max_length=2)
	slug = models.SlugField('Odnosnik', max_length=255, unique=True)
	uwagi = models.TextField(verbose_name='Uwagi', blank=True)
	ordering = ('nazwisko')
	class Meta:
		verbose_name = "Osoba"
		verbose_name_plural = "Osoby"
		db_table = 'szs_osoby'

	def __unicode__(self):
		return '%s %s' % (self.nazwisko, self.imie)

	def _get_full_name(self):
		"Zwraca Imie i Nazwisko."
		return '%s %s' % (self.nazwisko, self.imie)
		full_name = property(_get_full_name)

class Skladki(models.Model):
	kategoria = models.CharField('Kategoria', max_length=255)
	kwota_sk = models.DecimalField('Kwota składek', max_digits=6, decimal_places=2)
	rok = models.CharField('Rok', max_length = 5)

	class Meta:
		verbose_name = "Składka"
		verbose_name_plural = "Składki"
		db_table = 'szs_skladki'

	def __unicode__(self):
		return '%s %s' % (self.rok, self.kategoria)

class Wplaty(models.Model):
	oso = models.ForeignKey(Osoby, related_name='WplOso')
	skl = models.ForeignKey(Skladki, related_name='WplSkl')
	kwota_wpl = models.DecimalField('Kwota wpłaty', max_digits=6, decimal_places=2)
	d_wplaty = models.DateField('Data wpłaty', auto_now_add=False)
	uwagi = models.CharField('Uwagi', max_length=255, blank=True)
	add_date = models.DateTimeField('Data dodania', auto_now_add=True)

	class Meta:
		verbose_name = "Wpłata"
		verbose_name_plural = "Wpłaty"
		db_table = 'szs_wplaty'

	def __unicode__(self):
		return '%s %s %s' % (self.kwota_wpl, self.oso.nazwisko, self.oso.imie)

class Imprezy(models.Model):
	nazwa = models.CharField('Nazwa', max_length=255)
	miejsce = models.CharField('Miejsce', max_length=255)
	kwota = models.CharField('Kwota', max_length=255)
	data_od = models.CharField('Start', max_length=255)
	data_do = models.CharField('Koniec', max_length=255)
	zgloszenia = models.CharField('Zgłoszenia', max_length=255)
	info = models.CharField('Info', max_length=255)
	add_date = models.DateTimeField('Data dodania', auto_now_add=True)
	slug = models.SlugField('Odnosnik', max_length=255, unique=True)

	class Meta:
		verbose_name = "Impreza"
		verbose_name_plural = "Imprezy"
		db_table = 'szs_imprezy'

	def __unicode__(self):
		return self.nazwa

class Zgloszenia(models.Model):
	oso = models.ForeignKey(Osoby, related_name='ZglOso')
	imp = models.ForeignKey(Imprezy, related_name='ZglImp')
	add_date = models.DateTimeField('Data dodania', auto_now_add=True)
	slug = models.SlugField('Odnosnik', max_length=255, unique=True)

	class Meta:
		verbose_name = "Zgłoszenie"
		verbose_name_plural = "Zgłoszenia"
		db_table = 'szs_zgloszenia'

	def __unicode__(self):
		return self.imp


