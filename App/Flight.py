class Flight():

    def __init__(self, origin: str, origin_city: str, destination: str, destination_city: str, plane_type: str, traffic: str, flight_type: str, flight_duration: int, flight_distance: float):
        self.origin = origin
        self.origin_city = origin_city
        self.destination = destination
        self.destination_city = destination_city
        self.plane_type = plane_type
        self.traffic = traffic
        self.flight_type = flight_type
        self.flight_duration = flight_duration
        self.flight_distance = flight_distance