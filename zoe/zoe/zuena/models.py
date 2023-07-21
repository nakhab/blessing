from django.db import models

class EncryptedFile(models.Model):
    encrypted_file = models.FileField(upload_to='encrypted_files/')
    key_file = models.FileField(upload_to='key_files/')

