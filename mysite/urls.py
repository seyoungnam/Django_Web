from django.contrib import admin
from django.urls import path, include
from mysite.views import HomeView
# from django.conf.urls.static import static # photo
# from django.conf import settings # photo
from mysite.views import UserCreateView, UserCreateDoneTV # auth


# from bookmark.views import BookmarkLV, BookmarkDV

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')), # auth
    path('accounts/register/', UserCreateView.as_view(), name='register'), # auth
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'), # auth

    path('', HomeView.as_view(), name='home'),
    path('bookmark/', include('bookmark.urls')),
    path('blog/', include('blog.urls')),
    path('photo/', include('photo.urls')), #photo

    # # class-based views
    # path('bookmark/', BookmarkLV.as_view(), name='index'),
    # path('bookmark/<int:pk>', BookmarkDV.as_view(), name='detail')
]
#  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # photo
