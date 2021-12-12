from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
# from django.http import HttpResponse
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from .models import Post 
# Create your views here.

# posts = [
#     {
#         'author': 'benjaminn graham',
#         'title': 'The Intelligent Investor',
#         'content': 'Stock Investment',
#         'date_posted': 'November 29, 2021'
#     },
#     {
#         'author': 'Robert Kiyosaki',
#         'title': 'Rich Dad, Poor Dad',
#         'content': 'Thought About Money And Investing',
#         'date_posted': 'November 30, 2021'
#     }
# ]
def home(request):
	context = {
	   # 'posts': posts
	   'posts': Post.objects.all()

	}
	
	# data = Post.objects.all()
	return render(request, 'blog/home.html', context)


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_objects_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 4

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
    	form.instance.author = self.request.user
    	return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
    	form.instance.author = self.request.user
    	return super().form_valid(form)

    def test_func(self):
    	post = self.get_object()
    	if self.request.user == post.author:
    		return True
    	return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'
	
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False
     


def about(request):
	return render(request, 'blog/about.html',{'title': 'about'}) 
