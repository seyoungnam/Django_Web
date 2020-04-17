# 14.1.2. View : 모든 클래스형 뷰의 기본이 되는 최상위 뷰
class TestView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

# 14.1.3 TemplateView: 화면에 보여줄 템플릿 파일을 처리하는 간단한 뷰
class HomeView(TemplateView):
    template_name = 'home.html'     # home.html 템플릿 파일을 렌더링해서 화면에 보여줌

# 14.1.4 RedirectView : 주어진 URL로 redirect 시켜주는 제네릭 뷰
class TestRedirectView(RedirectView):
    url = '/blog/post/'
    # 아래처럼 URL 대신 패턴명을 지정해도 됨
    # pattern_name = 'blog:post_list'

# 14.1.5 DetailView: 특정 객체 하나에 대한 정보를 보여주는 뷰
class PostDV(DetailView):
    model = Post
    # 레코드 검색용 키는 URLconf에서 지정됨

# 14.1.6 ListView: 여러 객체의 리스트를 보여주는 뷰, 레코드에 대한 목록
class PostLV(ListView):
    model = Post        # object_list 컨텍스트 변수에 담아 템플릿에 넘겨줌

# 14.1.7. FormView: form을 보여주기 위한 제네릭 뷰
class SearchFormView(FormView):
    form_class = PostSearchForm
    # PostSearchForm은 아래와 같이 정의
    # from django import forms

    # class PostSearchForm(forms.Form):
    #     search_word = forms.CharField(label='Search Word')

    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list = Post.objects.filter(Q(title__icontains=searchWord)|
        Q(description__icontains=searchWord)|Q(content__icontains=searchWord)).distinct()
        
        context = {}
        context['form'] = form
        context['search_term'] = searchWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context)    # No Redirection(검색결과를 같은 페이지에 띄움)

# 14.1.8 CreateView: 새로운 레코드를 생성해서 테이블에 저장해주는 뷰, FormView 기능을 포함
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']    # form 만들 때 사용할 field
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')     # form 처리 성공후 도착 url
    # template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user     # form의 owner 필드에 현재 로그인한 사용자를 자동으로 채워줌
        return super().form_valid(form)

# 14.1.9 UpdateView: 기존 레코드 수정
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')
    # 수정할 레코드는 URLconf에서 지정
    # Exampe: /blog/99/update/
    # path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update')
    # 여기서 인자로 {'pk':99}를 넘겨줌

# 14.1.10 DeleteView
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    # UpdateView와 마찬가지로 URLconf에서 삭제할 객체의 인자를 받음

# 14.1.11 ArchiveIndexView: 여러 개의 객체를 날짜 기준으로 리스팅해주는 뷰
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'
    # 템플릿에 넘겨주는 컨텍스트 변수 중에서 object_list는 객체들의 리스트를, date_list는 연도를 담음

# 14.1.12 YearArchiveView: 연도가 주어지면 여러 개의 객체를 대상으로 가능한 월을 알려주는 제네릭 뷰
# 객체를 출력하는 것이 아니라 객체의 날짜 필드를 조사해 월을 추출
# 주어진 연도에 해당하는 객체들을 알고싶다면 make_object_list=True로 지정
class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True
    # 필요한 인자는 URLconf에서 추출
    # object_list: 객체 리스트(make_object_list=False면 object_list=None)
    # date_list: 객체들의 월

# 14.1.13 MonthArchiveView
# 주어진 연/월에 해당하는 객체를 보여주는 제네릭 뷰
# 연/월 인자는 URLconf에서 지정
# make_object_list 속성 없음
class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt' # 정렬기준 필드, 내림차순

# 14.1.14 WeekArchiveView
# 연/주가 주어지면 그에 해당하는 객체를 보여주는 제네릭 뷰
# 연/주 인자는 URLconf에서 지정
# 주는 1~55중 하나의 값을 가짐
# URLconf에 /blog/archive/2019/week/23/ 이 들어오면 {'year':2019, 'week':'23'}을 TestWeekArchiveView.as_view() 메소드에 넘겨줌
class TestWeekArchiveView(WeekArchiveView):
    model = Post
    date_field = 'modify_dt'

# 14.1.15 DayArchiveView
# 연/월/일이 주어지면 그에 해당하는 객체를 보여줌
# URLconf에 /blog/archive/2019/nov/10/이 들어오면 {'year':2019, 'month':'nov', 'day':10}을 PostDAV.as_view()에 넘겨줌
class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'

# 14.1.16 TodayArchiveView
# 오늘날짜에 해당하는 객체를 보여줌
# blog/archive/today/의 URL이 들어오면 뷰 내부에서 datetime.date.today() 함수로 오늘 날짜를 알아내 처리
class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'

# 14.1.17 DateDetailView
# 날짜 기준으로 특정 객체를 찾아서 그 객체의 상세정보를 보여주는 뷰
# /연/월/일/pk/ 등 4개 인자 필요
# /blog/archive/2019/nov/10/99/
class TestDateDetailView(DateDetailView):
    model = Post
    date_field = 'modify_dt'
# DateDetailView는 특정 객체 하나만 다룬다.
# 따라서 템플릿에 넘어가는 컨텍스트 변수는 object_list가 아니라 object 변수를 사용
# date_list 변수 사용 X





        


