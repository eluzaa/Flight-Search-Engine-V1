from amadeus import Client, ResponseError, Location
from typing import Dict, Any

# Initialize Amadeus client
amadeus = Client(
    client_id="WG2Uwh8VEaaZiSPRs3Ne1HddsrVgriqh",
    client_secret="QPGYfpeVMxW3IGon"
)

def get_airport_code(city_name: str) -> str:
    """
    Get the airport code for a given city name using Amadeus API.
    """
    try:
        response = amadeus.reference_data.locations.get(
            keyword=city_name,
            subType=Location.ANY
        )
        if response.data:
            # Return the code of the first result (usually the main airport)
            return response.data[0]['iataCode']
        else:
            return None
    except ResponseError as error:
        print(f"Error getting airport code for {city_name}: {str(error)}")
        return None

def search_flights(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Search for flights using Amadeus API.
    """
    print(params)
    print(type(params))
    try:
        # Convert city names to airport codes
        # origin_code = get_airport_code(params["Source city name"])
        # destination_code = get_airport_code(params["Destination city name"])

        origin_code = params["Source City Name"]
        destination_code = params["Destination City Name"]

        if not origin_code or not destination_code:
            return {"error": "Could not find airport code for one or both cities"}

        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin_code,
            destinationLocationCode=destination_code,
            departureDate=params['Date'],
            adults = 1,
            max = 2
            # adults=params.get('adults', 1),
            # travelClass=params.get('Traveller Class', 'ECONOMY')
        )
        return {"flights": response.data}
    except ResponseError as error:
        return {"error": str(error)}

# For testing purposes
if __name__ == "__main__":
    # Test search_flights
    search_params = {
        "Source city": "New York",
        "Destination city": "Los Angeles",
        "Date": "2024-08-15",
        "Traveller Class": "ECONOMY"
    }
    print(search_flights(search_params))