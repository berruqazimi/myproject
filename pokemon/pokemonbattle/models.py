from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    stats_change = models.IntegerField()
    show_id = models.IntegerField()

    def __str__(self):
        return self.name