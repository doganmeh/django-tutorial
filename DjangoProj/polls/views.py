from django.contrib import messages
from django.http import HttpResponse
from django.views import generic

from polls import models


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


#  parent view classes #############################################################################
def get_return_url(request):
    """
    for generic use; get "next" if available in GET, otherwise HTTP_REFERER
    """
    if 'next' in request.GET:
        return request.GET.get('next')
    return request.META.get('HTTP_REFERER')


class ListView(generic.ListView):
    template_name = 'common/list.html'  # to be overridden


class DetailView(generic.DetailView):
    exclude = ['id', ]


class CreateView(generic.CreateView):
    template_name = 'common/create.html'
    fields = []

    def form_valid(self, form):
        message_text = self.model.__name__ + ' is created.'
        messages.info(self.request, message_text)
        return super().form_valid(form)

    def get_success_url(self):
        return get_return_url(self.request)


class UpdateView(generic.UpdateView):
    template_name = 'common/update.html'
    fields = []
    
    def form_valid(self, form):
        message_text = self.model.__name__ + ' is updated.'
        messages.info(self.request, message_text)
        return super().form_valid(form)

    def get_success_url(self):
        return get_return_url(self.request)


class DeleteView(generic.DeleteView):
    template_name = 'common/delete.html'
    
    def delete(self, request, *args, **kwargs):
        message_text = self.model.__name__ + ' is deleted.'
        messages.info(self.request, message_text)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return get_return_url(self.request)


#  view classes ####################################################################################
class QuestionList(ListView):
    template_name = 'polls/question_list.html'
    model = models.Question


class QuestionDetail(DetailView):
    template_name = 'polls/question_detail.html'
    model = models.Question
    #fields = ['question_text', 'pub_date']


class QuestionCreate(CreateView):
    model = models.Question
    fields = ['question_text', 'pub_date']


class QuestionUpdate(UpdateView):
    model = models.Question
    fields = ['question_text', 'pub_date']


class QuestionDelete(DeleteView):
    model = models.Question
