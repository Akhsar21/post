from rest_framework.views import APIView
from rest_framework.response import Response


class UserDetailView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"email": request.user.email})
