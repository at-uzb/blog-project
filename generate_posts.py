import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone 
from datetime import timedelta
from posts.models import Post, Category
from faker import Faker
from users.models import User

fake = Faker()
    
def create_posts(num_posts=50):
    if not User.objects.exists():
        User.objects.create_user(username='admin', password='password')
    
    user = User.objects.first()
    category = Category.objects.first() or Category.objects.create(name="General")
    for _ in range(num_posts):
        post = Post.objects.create(
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=5),
            author=user,
            category=category,
            view_count=random.randint(0, 500),
        )

        random_days_ago = random.randint(0, 60)
        random_time = timezone.now() - timedelta(days=random_days_ago, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        post.created_at = random_time
        post.save()
    
if __name__ == "__main__":
    create_posts()
    print(f"Successfully created 50 sample posts.")