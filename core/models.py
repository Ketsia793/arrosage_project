from django.db import models

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.username


class Plante(models.Model):
    plante_id = models.BigAutoField(primary_key=True)
    name = models.CharField()
    moisture_max = models.BigIntegerField()
    moisture_min = models.BigIntegerField()

    def __str__(self):
        return self.name


class UserPlante(models.Model):
    users_plantes_id = models.BigAutoField(primary_key=True)
    name = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plante = models.ForeignKey(Plante, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.plante.name}'


