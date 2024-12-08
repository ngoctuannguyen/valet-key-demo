from datetime import timedelta, datetime
import base64
import hashlib
import hmac
import os
import time
from urllib.parse import urlencode
from django.conf import settings
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.utils import timezone
import urllib.parse
from .helpers import generate_valet_key_url
from .models import ValetKey
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden
from .models import ValetKey, Resource
from .forms import ResourceForm 
from django.views.decorators.csrf import csrf_exempt

def generate_valet_key(request):

    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to generate a valet key.")
    
    # file_path = None
    # expires_at = timezone.now() + timedelta(minutes=1)
    
    # if request.method == 'POST':
    #     file_path = request.POST.get('file_path')
    #     expires_at = request.POST.get('expires_at')

    #     if not file_path:
    #         return HttpResponseForbidden("Invalid input. Please provide both file path and expiration time.")
    #     if not expires_at:
    #         expires_at = timezone.now() + timedelta(minutes=1)
    #     else:
    #         try:
    #             expires_at = datetime.strptime(expires_at, '%Y-%m-%dT%H:%M')
    #         except ValueError:
    #             return HttpResponseForbidden("Invalid expiration time. Please provide a valid date and time in the format 'YYYY-MM-DDTHH:MM'.")

    # Valet key will be valid for 1 minute
    expires_at = timezone.now() + timedelta(minutes=1)

    valet_key = ValetKey.objects.create(user=request.user, 
                                        expires_at=expires_at,
                                        key=base64.b64encode(hashlib.sha256(os.urandom(32)).digest()).decode('utf-8'))
    
    print(valet_key.key)

    return render(request, 'valet_key.html', 
                  {'valet_key': "valet_key=" + str(valet_key.key), 
                   'expires_at': valet_key.expires_at})

SECRET_KEY = "eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4"  # This should match the key in helpers.py

def verify_valet_key(request):
    # Get parameters from URL
    document_id = request.GET.get("document_id")
    expiry = request.GET.get("expiry")
    signature = request.GET.get("signature")

    # Check if parameters are missing
    if not all([document_id, expiry, signature]):
        return HttpResponseForbidden("Invalid valet key.")

    # Verify the expiry time
    if int(expiry) < int(time.time()):
        return HttpResponseForbidden("Valet key expired.")

    # Recreate the message and verify the HMAC signature
    message = f"{document_id}:{expiry}"
    expected_signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_signature, signature):
        return HttpResponseForbidden("Invalid valet key signature.")

    # If verification passes, retrieve and return the document information
    document = get_object_or_404(Resource, id=document_id)
    return JsonResponse({"document_name": document.file.name, "file_path": document.file.path})


# Upload view that accepts a valet key for uploading
def upload_resource(request, valet_key):
    try:
        valet_key_instance = ValetKey.objects.get(key=valet_key)
    except ValetKey.DoesNotExist:
        return HttpResponseForbidden("Invalid valet key.")

    # Check if the valet key is valid
    if not valet_key_instance.is_valid():
        return HttpResponseForbidden("The valet key has expired or is inactive.")

    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploader = valet_key_instance.user  # Associate the resource with the valet key user
            resource.save()
            valet_key_instance.deactivate()  # Deactivate the valet key after use
            return redirect('upload_success') # Redirect to a success page
    else:
        form = ResourceForm()   

    return render(request, 'upload.html', {'form': form})

def upload_success(request):
    file_url = request.GET.get('file_url')
    return render(request, 'upload_successs.html', {'file_url': file_url})

@login_required
def valet_key_view(request):
    return generate_valet_key(request)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, 
                            username=username, 
                            password=password)
        if user is not None:
            login(request, user)
            return redirect('valet_key_view')
    return render(request, 'login.html')

@login_required
def resource_list(request):

    resources = Resource.objects.all()

    return render(request, 'resource_list.html', {'resources': resources})

def view_resources(request):
    return render(request, 'view_resources.html')

def protected_media(request, file_path):

    valet_key_ = request.GET.get('valet_key')

    if valet_key_ is None:
        return HttpResponseForbidden("Input your key")

    # Validate the valet key
    try:
        valet_key = ValetKey.objects.get(key=valet_key_)
        if not valet_key.is_valid() or valet_key is None:
            return HttpResponseForbidden("Invalid valet key or expired.")
    except ValetKey.DoesNotExist:
        return HttpResponseForbidden("Valet key not found.")

    media_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_path)
    media_file_path = os.path.normpath(media_file_path)

    # Serve the file if the key is valid
    if os.path.exists(media_file_path):
        return FileResponse(open(media_file_path, 'rb'))
    else:
        return HttpResponseForbidden("File not found.")