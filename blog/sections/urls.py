from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectionViewSet, ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'sections', SectionViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
