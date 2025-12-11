from rest_framework_simplejwt.tokens import RefreshToken

def scheme(request_data, serializer_class):
    serializer = serializer_class(data=request_data)
    if not serializer.is_valid():
        return {"success": False, "errors": serializer.errors}

    if hasattr(serializer, "create"):
        user = serializer.save()
    else:
        user = serializer.validated_data['user']

    refresh = RefreshToken.for_user(user)

    profile_data = {}
    if hasattr(user, "profile"):
        from .serializers import ProfileSerializer
        profile_data = ProfileSerializer(user.profile).data

    return {
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "national_id": user.national_id,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            "profile": profile_data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    }

