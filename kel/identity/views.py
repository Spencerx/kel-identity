from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

from oauth2_provider.models import AccessToken


def user_detail(request):
    return render(request, "user_detail.html", {})


def access_token_detail(request):
    if "access_token" not in request.GET:
        return JsonResponse({"error": "missing access_token"}, status=400)
    access_token = get_object_or_404(AccessToken, token=request.GET["access_token"])
    if access_token.is_expired():
        raise Http404()
    res = {
        "expires": access_token.expires,
        "user": {
            "id": access_token.user.id,
            "username": access_token.user.username,
        }
    }
    return JsonResponse(res)
