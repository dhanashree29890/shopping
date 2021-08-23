from django.db import models

from users.models import User

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
import uuid
from django.urls import path

# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, default=1)
    cost = models.FloatField()
    img = models.ImageField(upload_to="pics")
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)  # default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Products"
        # Add verbose name
        verbose_name = "Products List"


@receiver(models.signals.post_delete, sender=Products)
def auto_delete_file_on_delete(
    sender, instance, **kwargs
):  # delete song from audio folder
    """
    Deletes file from filesystem
    when object is deleted.
    """
    print("we are inside post delete")
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


@receiver(
    models.signals.pre_save, sender=Products
)  # deletes old img if changed during update
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when object is updated
    with new file."""

    if not instance.pk:
        return False
        print("returning now 1")
    try:
        old_img = sender.objects.get(pk=instance.pk).img
        print("we are in signal", old_img)
    except sender.DoesNotExist:
        print("returning now 2")
        return False
    if not old_img:
        print("returning now 3")
        return
    new_img = instance.img

    print("new img is", new_img)
    if not old_img == new_img:
        print("we are inside pre save")
        if os.path.isfile(old_img.path):
            os.remove(old_img.path)
