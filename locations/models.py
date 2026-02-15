from django.db import models


class State(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f'{self.name}, {self.state.name}'
