from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

# -----------------------------
# Login view (anonymous users)
# Limit: 5 requests per minute per IP
# -----------------------------
@csrf_exempt
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "Login successful"})
    
    return JsonResponse({"error": "Invalid credentials"}, status=401)


# -----------------------------
# Protected view (authenticated users)
# Limit: 10 requests per minute per IP
# -----------------------------
@login_required
@ratelimit(key='ip', rate='10/m', method='GET', block=True)
def protected_view(request):
    return JsonResponse({"message": "Authenticated access granted"})
