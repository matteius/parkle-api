from django.db import models


# Create your models here.
class ParklePlayer(models.Model):
    """ Consider this our User model for a Registered Parkle Player.
    """
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    player_key = models.CharField(max_length=32, unique=True)  # max length of uuid.hex
    secret_key = models.CharField(max_length=32, unique=True)
