from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=100, help_text="Character's name (e.g., 'Goblin Scout')")
    initiative = models.IntegerField(default=0, help_text="Initiative roll (higher goes first)")
    position = models.PositiveIntegerField(default=0, help_text="Order position (GM adjustable)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', '-initiative']  
    def __str__(self):
        return f"{self.name} (Init: {self.initiative})"
