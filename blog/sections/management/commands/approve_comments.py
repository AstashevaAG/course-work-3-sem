from django.core.management.base import BaseCommand

from ...models import Article, Comment


class Command(BaseCommand):
    help = 'Approve all comments in a specific article'

    def add_arguments(self, parser):
        parser.add_argument('article_id', type=int, help='ID of the article')

    def handle(self, *args, **options):
        article_id = options['article_id']

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Article with ID "{article_id}" does not exist.'))
            return

        comments_to_approve = Comment.objects.filter(article=article, is_approved=False)

        for comment in comments_to_approve:
            comment.is_approved = True
            comment.save()

        self.stdout.write(self.style.SUCCESS(f'Approved all comments in article with ID "{article_id}".'))

