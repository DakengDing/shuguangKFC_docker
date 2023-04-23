from django.db import models
from django.contrib.auth.models import User,AbstractUser

class Juntuan(models.Model):
    juntuan_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    #alliance = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Renwu(models.Model):
    game_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    juntuan = models.ForeignKey("Juntuan",on_delete=models.PROTECT)
    point = models.BigIntegerField(null=True,blank=True)
    user_name = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True)

    def __str__(self):
        return self.name


class Jiandui(models.Model):
    jiandui_id = models.BigAutoField(primary_key=True)
    fc_name = models.OneToOneField(Renwu,on_delete=models.PROTECT)
    timeCreate = models.DateTimeField(auto_now=True)
    spr = models.BooleanField(blank=False)
    member = models.JSONField()

    def __str__(self):
        return self.timeCreate



class Fc(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.PROTECT,primary_key=True)
    fc = models.BooleanField()



