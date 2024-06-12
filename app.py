from flask import Flask, request, jsonify
from clarke_wright import clarke_wright
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

class Route:
    def __init__(self, depot):
        self.depot = depot
        self.customers = []

    def add_customer(self, customer, savings):
        self.customers.append((customer, savings))


def calculate_distance(address1, address2):
    geolocator = Nominatim(user_agent="clarke_wright_app")
    try:
        location1 = geolocator.geocode(address1)
        location2 = geolocator.geocode(address2)
        if location1 is None or location2 is None:
            return None
        return geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).kilometers
    except GeocoderTimedOut:
        return None


@app.route('/optimize', methods=['POST'])
def optimize_routes():
    data = request.get_json()
    customer_addresses = data.get('customer_addresses')
    depot_address = data.get('depot_address')
    capacity = data.get('capacity')

    distances = {}
    for customer_address in customer_addresses:
        distance = calculate_distance(depot_address, customer_address)
        if distance is not None:
            distances[customer_address] = distance

    sorted_distances = sorted(distances.items(), key=lambda x: x[1])

    customers = [address for address, _ in sorted_distances]

    depot_coordinates = Nominatim(user_agent="clarke_wright_app").geocode(depot_address)
    if depot_coordinates is None:
        return jsonify({'error': 'Failed to geocode depot address'}), 400
    depot_coordinates = (depot_coordinates.latitude, depot_coordinates.longitude)

    optimized_routes = clarke_wright(customers, depot_coordinates, capacity)

    routes_data = []
    for route in optimized_routes:
        route_data = {
            'depot': depot_address,
            'customers': [{'address': customer, 'savings': savings} for customer, savings in route.customers]
        }
        routes_data.append(route_data)

    return jsonify(routes_data)

if __name__ == '__main__':
    app.run(debug=True)
