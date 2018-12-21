from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.flatpages.models import FlatPage

@method_decorator(login_required, name='dispatch')
class Home(ListView):
    model = User
    template_name = 'intra/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # posts = Post.objects.all().filter(is_public=False)
        # products = Article.objects.all()

        # if products.exists():
        #     context['products_len'] = products.count()

        # if posts.exists():
        #     if len(posts)>1:
        #         context['have_many_posts'] = True
        #     context['posts'] = posts
        #     context['post_len'] = len(posts)

        context['menu'] = 'home'
        context['SITE_URL'] = 'Intra'
        context['users_len'] = self.model.objects.count()
        context['APP'] = 'Intra'
        return context