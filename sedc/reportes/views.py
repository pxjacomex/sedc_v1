from django.views.generic.base import TemplateView

class ReportesPageView(TemplateView):

    template_name = "reportes.html"

    def get_context_data(self, **kwargs):
        context = super(ReportesPageView, self).get_context_data(**kwargs)
        return context
