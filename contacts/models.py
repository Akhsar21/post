from django.db import models

STATUS = (
    (1, 'New'),
    (2, 'Read'),
)


class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=255)
    status = models.IntegerField(choices=STATUS, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
