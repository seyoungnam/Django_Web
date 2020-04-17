# 14.2.1 속성 오버라이딩
# 개발자가 속성을 변경해서 사용하는 경우를 속성 오버라이딩이라고 함

# model
# View, TemplateView, RedirectView, FormView를 제외하고 모든 제네릭 뷰에서 사용
class TestPostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

# queryset
# View, TemplateView, RedirectView, FormView를 제외하고 모든 제네릭 뷰에서 사용
# 작업 대상이 되는 QuerySet 객체를 지정
class TestPostLV(ListView):
    #model = Post
    queryset = Post.objects.all()[:5]   # Post 리스트를 모두 보여주는 것이 아니라 5개만 보여주고 싶을 때 사용
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

# template_name
# 모든 제네릭 뷰에서 사용, 템플릿 파일명 지정

# context_object_name
# 기본뷰(View, TemplateView, RedirectView) 제외하고 모든 제네릭 뷰에서 사용
# 템플릿 파일에서 사용할 컨텍스트 변수명을 지정

# paginate_by
# ListView와 날짜 기반 뷰에서 사용
# 페이지당 몇 개 항목을 출력할지 정수로 지정
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

# date_field
# 날짜 기반 뷰에서 기준이 되는 필드를 지정, 이 필드 기준으로 연/월/일 검사
# 이 필드의 타입은 DateField 혹은 DateTimeField 여야 함
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'

# make_object_list
# YearArchiveView 사용 시 해당 년에 맞는 객체 리스트를 생성할지 여부를 지정
# True이면 객체 리스트를 만들고, False면 None이 할당
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True

# form_class
# FormView, CreateView, UpdateView에서 사용
# form 만드는데 사용할 클래스 지정
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

# in forms.py
from django import forms

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')

# initial
# FormView, CreateView, UpdateView에서 사용
# form에 사용할 초기 데이터를 dict({})으로 지정
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# fields
# CreateView, UpdateView에서 사용
# form에 사용할 필드 지정
# ModelForm 클래스의 Meta.fields 속성과 동일

# success_url
# FormView, CreateView, UpdateView, DeleteView에서 사용
# form 처리 성공한 후 리다이렉트될 URL을 지정
class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    success_url = reverse_lazy('blog:index')



# 14.2.2 메소드 오버라이딩

# get_queryset()
# 기본뷰(View, TemplateView, RedirectView)와 FormView 제외하고 모든 제네릭 뷰에 사용
# 출력 객체 검색하기
class TestPostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(Q(content__icontains=self.kwargs['word'])).distinct()

# get_context_data(**kwargs)
# 모든 제네릭 뷰에서 사용
# 템플릿에서 사용할 데이터를 찾고 수정하여 컨텍스트로 반환
class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag')) # 주의! tags_name이 아니라 tags__name 이다.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context

# form_valid(form)
# FormView, CreateView, UpdateView에서 사용
# get_success_url() 메소드가 반환하는 URL로 리다이렉트를 수행
class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord) | Q(content__icontains=searchWord)).distinct()

        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)  # No Redirection
