from rest_framework.decorators import api_view
from .services import FlightService
from .seralizers import FlightSerializer, FlightRangeSerializer
from rest_framework.response import Response

flight_service = FlightService()

@api_view(['GET'])
def get_flight(request):
    data = request.query_params
    serializer = FlightSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    response = flight_service.fetch_flight(serializer.validated_data)
    return Response(response)

@api_view(['GET'])
def get_flights_range(request):
    data = request.query_params
    serializer = FlightRangeSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    response = flight_service.search_flights_in_range(serializer.validated_data)
    return Response(response)




    

