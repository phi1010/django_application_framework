import uuid

from django.db import models

class MyModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    some_second_id = models.CharField(max_length=256, unique=True, db_index=True)
    display_name = models.TextField()
    order = models.IntegerField(help_text="Order of appearance for door buttons. Lower is higher up.", default=42)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return f"MyModel({self.some_second_id=!r}, {self.display_name=!r})"
