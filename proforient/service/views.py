from django.shortcuts import render, get_object_or_404, redirect
from service.models import Services, Categories, Comments
from service.forms import CreateServiceForm
from modelUtils.emailSignInModel import EmailSignInUser
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from specialist.models import SpecialistProfile
from user.models import Profile
from modelUtils.emailSignInModel import EmailSignInUser
from modelUtils.userUtils import userDefine
# Create your views here.

def _paginate(objects_list, request, page=None):
    objects_page = []

    if not page:
        page = request.GET.get('page')

    paginator = Paginator(objects_list, 12)

    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        page = int(page)
        if page < 1:
            objects_page = paginator.page(1)
        elif page > paginator.num_pages:
            objects_page = paginator.page(paginator.num_pages)
    return objects_page


def allServicesPage(request):
    current_usr = userDefine(request)
    services = _paginate(Services.objects.allServices(),request)
    context = {
        'current_usr': current_usr,
        'services': services
    }
    return render(request, 'service/services.html', context)


def servicesByCategoryPage(request, category_name):
    current_usr = userDefine(request)
    services = _paginate(Services.objects.allServicesByCategory(categoryName=category_name),request)
    context = {
        'current_usr': current_usr,
        'services': services
    }
    return render(request, '.html', context)


def servicePage(request, id):
    current_usr = userDefine(request)
    service = get_object_or_404(Services,pk=id)
    context = {
        'current_usr': current_usr,
        'service': service
    }
    return render(request, 'service/service.html', context)


def createService(request):
    if request.method == 'GET':
        form = CreateServiceForm()
    elif request.method == 'POST':
        form = CreateServiceForm(request.POST)
        if form.is_valid():
            if request.user is None or request.user.id is None:
                raise Http404
            user = SpecialistProfile.objects.get(user_id=request.user.id)
            serv = Services.objects.createService(
                user,
                form.cleaned_data['category'],
                form.cleaned_data['title'],
                form.cleaned_data['description'],
                form.cleaned_data['price']
            )
            return redirect('servicePage', id=str(serv.pk))
    context = {
        'form': form
    }

    return render(request, 'service/create_service.html', context)


