# Create your views here.
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template import Context, loader

from blog.models import Blog

def _page_blogs(page):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 5)
    try: blogs = paginator.page(page)
    except: blogs = paginator.page(1)
    return blogs

def _archive_generator():
    from blog.models import YEARS
    from blog.models import MONTHS
    archives = {}
    for y in YEARS:
        y_c = Blog.objects.filter(year=y).count()
        if y_c:
            archives[y] = {'months': {}}
            for m in MONTHS:
                m_c = Blog.objects.filter(year=y, month=m[0]).count()
                if m_c: archives[y]['months'][m[1]] = m_c
    return archives

def blog_archive(request, year, month):
    return HttpResponse('hi')

def blog_page(request, page):
    template = loader.get_template('blog/left.html')
    context = Context({"blogs": _page_blogs(page)})
    return HttpResponse(template.render(context))

def index(request):
    blogs = _page_blogs(1)
    archives = _archive_generator()
    template = loader.get_template('blog/index.html')
    context = Context({"blogs": blogs, 'archives': archives})
    return HttpResponse(template.render(context))
