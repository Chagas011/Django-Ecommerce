
from django.views.generic import UpdateView
from django.http import HttpResponse


class Update(UpdateView):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')
