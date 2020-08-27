from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Movie, UserProxy, ButtonBox


class IndexView(ListView):
    model = Movie
    template_name = 'buttons/index.html'
    context_object_name = 'movies'


class MovieView(DetailView):
    model = Movie
    template_name = 'buttons/movie.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        action_dict = {
            'mark_seen': 'mark_seen',
            'unmark_seen': 'unmark_seen',
            'mark_favorite': 'mark_favorite',
            'unmark_favorite': 'unmark_favorite',
            'mark_watch': 'mark_watch', # bug note: you got No Reverse Match because the key here was 'mark_watch_list'
            'unmark_watch': 'unmark_watch', # and you were passing actions.mark_watch in the url tag.
        }

        if ButtonBox.objects.filter(movie=self.object, user=self.request.user).exists():
            box_data = ButtonBox.objects.get(movie=self.object, user=self.request.user)
        else:
            box_data = None


        context['actions'] = action_dict
        context['box_data'] = box_data

        return context # holy shit you forgot to put this here AGAIN.

class CreateButtonBox(CreateView):
    model = ButtonBox
    fields = []


    def form_valid(self, form):
        # get the movie object via name captured from URLconf, packed in kwargs, stored in self (of this view instance)
        movie = Movie.objects.get(id=self.kwargs['pk']) # this is failing; do tests here, try to verify what values are arriving from
                                                          # self.kwargs, etc.

        form.instance.user = self.request.user
        form.instance.movie = movie

        if self.kwargs['action'] == 'mark_seen':
            form.instance.seen = True
        if self.kwargs['action'] == 'mark_favorite':
            form.instance.favorite = True
        if self.kwargs['action'] == 'mark_watch':
            form.instance.watch = True

        return super().form_valid(form) # saves the form

    def get_success_url(self):
        return reverse('buttons:movie', kwargs={'pk': self.object.movie.id}) # self is the view, .object is the ButtonBox object, .movie is
                                                                             # a field on the ButtonBox object (linked to a movie object), .id
                                                                             # is a field on the movie object.



class UpdateButtonBox(UpdateView):
    model = ButtonBox
    fields = []

    def form_valid(self, form):

        action = self.kwargs['action']

        if action == 'mark_seen':
            form.instance.seen = True

        elif action == 'unmark_seen':
            form.instance.seen = False

        elif action == 'mark_favorite':
            form.instance.seen = True
            form.instance.favorite = True

        elif action == 'unmark_favorite':
            form.instance.favorite = False

        elif action == 'mark_watch':
            form.instance.watch = True

        elif action == 'unmark_watch':
            form.instance.watch = False

        else:
            pass

        return super().form_valid(form)  # form gets saved


    def get_success_url(self):
        return reverse('buttons:movie', kwargs={'pk': self.object.movie.id})




