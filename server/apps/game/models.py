from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    name = None
    nickname = None
    birth = None
    gender = None
    job = None
    desc = None
    email = models.EmailField(null=True)
    # 점수
    score = models.IntegerField(default=0)


class Play(models.Model):
    how_to_win = ["숫자가 더 작은 사람이 대결에서 이깁니다", "숫자가 더 큰 사람이 대결에서 이깁니다"]
    # 공격한 사람 -> 처음에 정해짐
    attack_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="attack")
    # 공격당한 사람 -> 처음에 정해짐
    defend_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="defend")
    # 공격한 사람 카드 -> 처음에 정해짐
    attack_card = models.IntegerField()
    # 공격당한 사람 카드 -> 반격하기 할 때 업데이트
    defend_card = models.IntegerField(blank=True, default=0)
    # 반격하기 여부
    accept = models.BooleanField(default=False)
    # 결과
    winner = models.IntegerField(blank=True, default=0)
    # 이기는 기준
    rule = models.IntegerField(blank=True, default=0)
    pass
