from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from uuid import uuid4


# content_type = ContentType.objects.get_for_model(Vote)
# permission = Permission.objects.create(
#    codename='can_see_vote_count',
#    name='Can See Vote Count',
#    content_type=content_type,
# )

# class Meta:
#     permissions = (
#                    ("view_student_reports", "can view student reports"),
#                    ("find_student_vote", "can find a student's vote"),
#                   )


class User(AbstractUser):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    slug = models.CharField(max_length=50, unique=True, default=uuid4)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self) -> str:
        return self.email
