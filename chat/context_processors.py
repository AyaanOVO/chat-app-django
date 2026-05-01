from .models import FriendRequest

def request_data(request):
    if request.user.is_authenticated:
        count = FriendRequest.objects.filter(
            receiver=request.user,
            accepted=False
        ).count()
    else:
        count = 0

    return {
        "pending_requests_count": count
    }