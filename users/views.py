
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from users.models import User
# from users.serializers import UserSerializer
# from roombooking.decorators import role_required

# class CreateUserView(APIView):
#     @role_required('admin')
#     def post(self, request):
#         print("request.data",request.data)
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
