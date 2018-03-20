from django.core.paginator import Paginator
def pagination(lista,page,num_reg):
    #lista=model.objects.all()
    paginator = Paginator(lista, num_reg)
    factor=paginator.num_pages//2
    if factor>5:
        factor=5
    if page is None:
        page=1
    else:
        page=int(page)
    if page == 1:
        start=1
        last=factor
    elif page == paginator.num_pages:
        last=paginator.num_pages
        start=last-1
    elif (page-factor)<0:
        start=1
        last=factor
    elif page>(paginator.num_pages-factor):
        start=page-factor
        last=paginator.num_pages
    else:
        start=page-factor//2
        last=page+factor//2
    context={
        'first':'1',
        'last':paginator.num_pages,
        'range':range(start,last+1),
    }
    return context
