from rest_framework.decorators import api_view
from .services import FlightService
from .seralizers import FlightSerializer
from rest_framework.response import Response

flight_service = FlightService()

@api_view(['GET'])
def get_flight(request):
    data = request.query_params
    serializer = FlightSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    response = flight_service.get_flight(serializer.validated_data)
    return Response(response)
    

