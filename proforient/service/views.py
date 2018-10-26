from django.shortcuts import render, get_object_or_404
from service.models import Services, Categories, Comments
from service.forms import CreateServiceForm
from modelUtils.emailSignInModel import EmailSignInUser
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
    services = _paginate(Services.objects.allServices(),request)
    context = {
        'services': services
    }
    return render()


def servicesByCategoryPage(request, category_name):
    services = _paginate(Services.objects.allServicesByCategory(categoryName=category_name),request)
    context = {
        'services': services
    }
    return render()


def servicePage(request, id):
    service = get_object_or_404(Services,pk=id)
    context = {
        'service': service
    }
    return render()


def createService(request, category):
    if request.method == 'GET':
        form = CreateServiceForm()
    elif request.method == 'POST':
        form = CreateServiceForm(request.POST)
        if form.is_valid():
            if request.user is None or request.user.id is None:
                raise Http404
            user = EmailSignInUser.objects.get(user_id=request.user.id)
            serv = Services.objects.createService(
                user,
                category,
                form.cleaned_data['title'],
                form.cleaned_data['description'],
                form.cleaned_data['price']
            )

            return redirect('service/' + str(serv.pk))
    context = {
        'form': form
    }

    return render()


