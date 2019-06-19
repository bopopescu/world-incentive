import bleach
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.utils.translation import get_language_from_request
from django.views import View
from django.utils.translation import gettext as _

from initiative.forms import CreateInitiativePromptForm, InitiativeForm
from initiative.models import InitiativeLanguage, InitiativeVersion, Initiative


class ShowInitiativeView(View):
    def get(self, request, initiative_pk):
        lang = request.GET.get('lang', '')
        language_codes = lang.split(',')
        if language_codes == ['']:
            language_codes = []

        initiative = get_object_or_404(Initiative, pk=initiative_pk)
        lang_obj = initiative.first_of_specified_languages(language_codes)
        version = lang_obj.last_version if lang_obj else None

        old_versions = lang_obj and lang_obj.versions.order_by('-id')

        problem = version and mark_safe(bleach.clean(version.problem, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        solution = version and mark_safe(bleach.clean(version.solution, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        outcome = version and mark_safe(bleach.clean(version.outcome, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        return render(request, 'initiative/view.html', {'version': version,
                                                        'old_versions': old_versions,
                                                        'problem': problem,
                                                        'solution': solution,
                                                        'outcome': outcome,
                                                        'is_last_version': bool(version),
                                                        'lang': lang})


class ListInitiativeView(View):
    def get(self, request):
        lang = request.GET.get('lang', '')
        language_codes = lang.split(',')
        if language_codes == ['']:
            language_codes = []
        cat = request.GET.get('cat', '')
        categories = cat.split(',')
        if categories == ['']:
            categories = []

        if language_codes == []:
            lang_code = get_language_from_request(request, check_path=True)
            language_codes = [lang_code]

        lst = Initiative.objects.filter(languages__language__in=language_codes)
        if categories:
            lst = lst.filter(categories__pk__in=categories)
        lst = lst.distinct('pk').order_by('-pk')

        paginator = Paginator(lst, 25)
        page = request.GET.get('page')
        initiatives = paginator.get_page(page)

        versions = (i.version_in_specified_languages(language_codes) for i in initiatives)

        # Remove duplicate content
        # nofollow = not InitiativeLanguage.objects.filter(language__in=language_codes).exists()

        return render(request, 'initiative/list.html',
                      {'versions': versions,
                       'paginator': paginator,
                       'page_obj': initiatives})


class ShowInitiativeVersionView(View):
    def get(self, request, version_pk):
        version = get_object_or_404(InitiativeVersion, pk=version_pk)
        lang_obj = version.initiative_language
        old_versions = lang_obj.versions.order_by('-id')

        problem = mark_safe(bleach.clean(version.problem, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        solution = mark_safe(bleach.clean(version.solution, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        outcome = mark_safe(bleach.clean(version.outcome, tags=bleach.sanitizer.ALLOWED_TAGS + ['p', 'br']))
        return render(request, 'initiative/view.html', {'version': version,
                                                        'old_versions': old_versions,
                                                        'problem': problem,
                                                        'solution': solution,
                                                        'outcome': outcome,
                                                        'is_last_version': version == lang_obj.last_version})


class CreateInitiativePromptView(LoginRequiredMixin, View):
    def get(self, request):
        language = get_language_from_request(request)
        form = CreateInitiativePromptForm(initial={'language': language})
        return render(request, 'initiative/create-initiative-prompt.html', {'form': form})


class CreateInitiativeView(LoginRequiredMixin, View):
    def get(self, request):
        language = request.GET.get('language', 'en')
        form = InitiativeForm(initial={'language': language})
        return render(request, 'initiative/initiative-form.html', {'form': form})

    def post(self, request):
        form = InitiativeForm(request.POST)
        form.fields['editor'] = request.user
        form.save()
        return render(request, 'initiative/initiative-form.html', {'form': form})  # FIXME
