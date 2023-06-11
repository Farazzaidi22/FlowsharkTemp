from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from .serializers import * 
from .models import *
from .utils import *
import json 

# Create your views here.
class TickerFilterView(APIView):
    def post(self, request):
        serializer = TickerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            fm_payload = {k: v for k, v in serializer.data.items() if v is not None}
            result = get_dataframe(fm_payload)

            serialized = TickerSerializer(result, many=True)
            return Response(serialized.data, status=status.HTTP_202_ACCEPTED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ticker_data = Ticker.objects.all()
        serializer = TickerSerializer(ticker_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


