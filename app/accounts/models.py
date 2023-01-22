from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user, get_user_model
import uuid
# Create your models here.



class CustomUser(AbstractUser, UserManager):

    email = models.EmailField(verbose_name="メールアドレス", unique=True, blank=False, null=False)  #emailを必須＆ユニークに設定
    thumbnail = models.ImageField(verbose_name="プロフィール画像",upload_to="images/thumbnail/", blank=True, null=True)
    comment = models.CharField(verbose_name="ひとことコメント",max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_status = models.CharField(verbose_name="ユーザステータス",choices=[("A","online"),("B","offline"),("C","busy")], max_length=50)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    USERNAME_FIELD = 'email'   #ログオンIDをユーザ名→Emailへ変更
    REQUIRED_FIELDS = ['username']       #ユーザーを作成するために必要なキーを指定

User = get_user_model()

class Friend(models.Model):
    follo_id = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_id = models.UUIDField(editable=False)
    relation = models.BooleanField(verbose_name="関係",default=False)
    status = models.CharField(verbose_name="ステータス",choices=[("A","フォロー中"),("-A","フォローされている"),("C","ブロックしている"),("-C","ブロックされている"),("D","削除されたアカウント")], max_length=50)
