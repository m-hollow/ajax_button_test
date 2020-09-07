from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Movie, ButtonBox
from .forms import ButtonBoxForm

class IndexView(ListView):
    model = Movie
    template_name = 'buttons/index.html'
    context_object_name = 'movies'


class MovieView(DetailView):
    model = Movie
    template_name = 'buttons/movie_two.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if ButtonBox.objects.filter(movie=self.object, user=self.request.user).exists():
            box_data = ButtonBox.objects.get(movie=self.object, user=self.request.user)
        else:
            box_data = None

        context['box_data'] = box_data

        return context # holy shit you forgot to put this here AGAIN.


def mark_seen_view(request):

    data = {'success': False }

    if request.method == 'POST':
        user = request.user
        movie_id = request.POST.get('movie_id', None)

        movie = Movie.objects.get(id=movie_id)

        if ButtonBox.objects.filter(user=user, movie=movie).exists():
            box_ob = ButtonBox.objects.get(user=user, movie=movie)
            message = 'Retrieved existing box object | '
        else:
            box_ob = ButtonBox(user=user, movie=movie)
            message = 'Created a new box object | '

        # if current state is False, switch it to true, and notify ajax function of new status via 'seen' in data
        if not box_ob.seen:
            box_ob.seen = True
            message += 'Seen now set to True'
            data['seen'] = True
        # current state is True, so toggle it to False
        else:
            box_ob.seen = False
            box_ob.favorite = False     # do not allow favorite = True for a movie that is not Seen
            message += 'Seen and Favorite now set to False'
            data['seen'] = False

        box_ob.save()

        data['success'] = True
        data['message'] = message

        return JsonResponse(data)

def mark_fav_view(request):

    data = {'success': False }

    if request.method == 'POST':
        user = request.user
        movie_id = request.POST.get('movie_id', None)

        movie = Movie.objects.get(id=movie_id)

        if ButtonBox.objects.filter(user=user, movie=movie).exists():
            box_ob = ButtonBox.objects.get(user=user, movie=movie)
            message = 'Retrieved existing box object | '
        else:
            box_ob = ButtonBox(user=user, movie=movie)
            message = 'Created a new box object | '

        # if current state is False, switch it to true, and notify ajax function of this via 'fav' in data
        if not box_ob.favorite:
            box_ob.seen = True     # if user is turning Fav to True, then make sure Seen is also True
            box_ob.favorite = True
            message += 'Favorite now set to True'
            data['fav'] = True
        else:
            box_ob.favorite = False
            message += 'Favorite now set to False'
            data['fav'] = False

        box_ob.save()

        data['success'] = True
        data['message'] = message

        return JsonResponse(data)

def mark_watch_view(request):

    data = {'success': False }

    if request.method == 'POST':
        user = request.user
        movie_id = request.POST.get('movie_id', None)

        movie = Movie.objects.get(id=movie_id)

        if ButtonBox.objects.filter(user=user, movie=movie).exists():
            box_ob = ButtonBox.objects.get(user=user, movie=movie)
            message = 'Retrieved existing box object | '
        else:
            box_ob = ButtonBox(user=user, movie=movie)
            message = 'Created a new box object | '

        # if current state is False, switch it to true, and notify ajax function of this via 'watch' in data
        if not box_ob.watch:
            box_ob.watch = True
            message += 'Watchlist now set to True'
            data['watch'] = True
        else:
            box_ob.watch = False
            message += 'Watchlist now set to False'
            data['watch'] = False

        box_ob.save()

        data['success'] = True
        data['message'] = message

        return JsonResponse(data)


class CreateButtonBox(CreateView):
    model = ButtonBox
    fields = []


    def form_valid(self, form):
        # get the movie object via name captured from URLconf, packed in kwargs, stored in self (of this view instance)
        movie = Movie.objects.get(id=self.kwargs['pk'])

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

    # interesting note:
    # form_valid is called -after- a form passes .is_valid (bool result);
    # I think the only reason this is sending 'True' and THEN allowing you to
    # update attributes is because you have fields = [] above, that is, no
    # listed fields. Therefore there is nothing for it to check as 'valid',
    # is_valid() returns true, then form_valid is called and your manual
    # updates to attribute values are performed.
    # since there is no actual form data, there is nothing to validate.
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






































