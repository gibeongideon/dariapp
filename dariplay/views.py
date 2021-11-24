from rest_framework import viewsets, generics
from .serializers import MatchSerializer
from .models import Match
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MatchRecordView(APIView):

    def get(self, format=None):
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = MatchSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": True, "error_msg": serializer.error_messages,},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    search_fields = ("user",)        
class MatchView(generics.RetrieveAPIView):
    ''' Main View to return all files per project'''

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
