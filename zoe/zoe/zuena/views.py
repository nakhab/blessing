from django.shortcuts import render
from django.http import HttpResponse
from .forms import EncryptForm
from .models import EncryptedFile
from cryptography.fernet import Fernet

def encrypt_file_or_text(file_content, key):
    fernet = Fernet(key)
    encrypted_content = fernet.encrypt(file_content)
    return encrypted_content

def decrypt_file(encrypted_file, key):
    fernet = Fernet(key)
    decrypted_content = fernet.decrypt(encrypted_file)
    return decrypted_content

def encrypt_view(request):
    if request.method == 'POST':
        form = EncryptForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            text = form.cleaned_data['text']
            key = Fernet.generate_key()

            if file:
                encrypted_content = encrypt_file_or_text(file.read(), key)
                encrypted_file = EncryptedFile.objects.create(encrypted_file=encrypted_content, key_file=key)
            elif text:
                text = text.encode('utf-8')
                encrypted_content = encrypt_file_or_text(text, key)
                encrypted_file = EncryptedFile.objects.create(encrypted_file=encrypted_content, key_file=key)

            return render(request, 'encrypted.html', {'encrypted_file': encrypted_file})
    else:
        form = EncryptForm()

    return render(request, 'encrypt.html', {'form': form})

def download_file(request, file_id):
    encrypted_file = EncryptedFile.objects.get(pk=file_id)
    response = HttpResponse(encrypted_file.encrypted_file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{encrypted_file.encrypted_file.name}"'
    return response

def decrypt_view(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        key = request.POST.get('key')

        try:
            encrypted_file = EncryptedFile.objects.get(pk=file_id)
            decrypted_content = decrypt_file(encrypted_file.encrypted_file, key.encode('utf-8'))

            response = HttpResponse(decrypted_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="decrypted_{encrypted_file.encrypted_file.name}"'
            return response
        except (EncryptedFile.DoesNotExist, ValueError):
            return HttpResponse('Invalid file ID or key.')

    return render(request, 'decrypt.html')
