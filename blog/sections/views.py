from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Section, Article, Comment
from .pagination import ArticlePagination, CommentPagination
from .serializers import SectionSerializer, ArticleSerializer, CommentSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    # permission_classes = [permissions.IsAdminUser]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    # permission_classes = [permissions.IsAuthenticated]
    pagination_class = ArticlePagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    @action(methods=['GET'], detail=False)
    def get_articles_without_comments(self, request):
        section_id = request.query_params.get('section_id')
        articles = Article.objects.filter(
            Q(section_id=section_id) & ~Q(comments__isnull=False) | (
                        Q(section_id=section_id) & Q(comments__is_approved=False))
        )
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def get_articles_to_searchword(self, request):
        search_word = request.query_params.get('search_word')
        articles = Article.objects.filter(
            (Q(title__icontains=search_word) | Q(content__icontains=search_word) | Q(comments__content__icontains=search_word)) & ~Q(comments__is_approved=False)
        ).distinct()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def add_comment(self, request, pk=None):
        article = self.get_object()
        data = {'content': request.data.get('content')}

        serializer = CommentSerializer(data={'content': data.get('content'), 'article': article.pk, 'created_by': request.user.id})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    # permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)