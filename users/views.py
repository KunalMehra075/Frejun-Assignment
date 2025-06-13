from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
from roombooking.permissions import IsManagerOrAdmin
from roombooking.utils import StandardResultsSetPagination
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UsersView(APIView):
    """
    API endpoint for managing users.
    
    GET: Retrieve a paginated list of all users
    """
    permission_classes = [IsManagerOrAdmin]
    pagination_class = StandardResultsSetPagination
    
    def get(self, request):
        """
        Retrieve a paginated list of all users.
        Only accessible by managers and administrators.
        
        Query Parameters:
            page: Page number (default: 1)
            page_size: Number of items per page (default: 10, max: 100)
        """
        queryset = User.objects.all().order_by('-id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
