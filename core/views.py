import html

from django import views
from django.contrib.sitemaps import Sitemap
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _, LANGUAGE_SESSION_KEY

from core.models import RegionLevel
from initiative.models import Initiative, InitiativeVersion, InitiativeLanguage
from user.models import User


class SetLanguageView(views.View):
    def post(self, request):
        request.session[LANGUAGE_SESSION_KEY] = request.POST.get('lang', 'en')
        return HttpResponse('ok')


class CitiesAjaxView(views.View):
    def get(self, request, level, parent_pk):
        try:
            klass = RegionLevel.get_model(level + 1)
            parent_rel = {
                RegionLevel.LEVEL_COUNTRY: 'country_id',
                RegionLevel.LEVEL_REGION: 'region_id',
                RegionLevel.LEVEL_SUBREGION: 'subregion_id',
                RegionLevel.LEVEL_CITY: 'city_id',
            }[level]
        except KeyError:
            return HttpResponse(_("Wrong level"), status=400)
        lst = klass.objects.filter(**{parent_rel: parent_pk}).order_by('name').only('pk', 'name')
        return HttpResponse("\n".join(["<option value='%d'>%s</option>" % (item.pk, html.escape(item.name)) \
                                       for item in lst]))


class StaticViewSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return ['mainpage']

    def location(self, item):
        return reverse(item)


class InitiativeSitemap(Sitemap):
    priority = 1.0

    def items(self):
        # TODO:
        # return Initiative.objects.filter(spam=False)
        return InitiativeLanguage.objects.filter()

    def lastmod(self, obj):
        return obj.initiative.updated  # TODO: wrong date


class InitiativeVersionSitemap(Sitemap):
    priority = 0.3

    def items(self):
        return InitiativeVersion.objects.filter(spam=False)

    def lastmod(self, obj):
        return obj.created


class UserSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return User.objects.filter()
