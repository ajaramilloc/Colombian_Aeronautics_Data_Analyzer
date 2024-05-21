from Airport import Airport
from Flight import Flight
from Graph import Graph

from math import radians, sin, cos, sqrt, atan2
from typing import Tuple, List, Dict

# Global data structures
airports: Dict[str, Airport] = {}
flights: List[Flight] = []

commercial_digraph = Graph()
commercial_graph = Graph(False)
military_digraph = Graph()
military_graph = Graph(False)
cargo_digraph = Graph()
cargo_graph = Graph(False)
general_digraph = Graph()
general_graph = Graph(False)

def read_airports(file_path: str) -> Dict[str, Airport]:
    """
    Reads airport data from a CSV file and returns a dictionary of Airport objects.

    Parameters:
    file_path (str): The path to the CSV file containing airport data.

    Returns:
    Dict[str, Airport]: A dictionary with ICAO codes as keys and Airport objects as values.
    """
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            airport_data = line.strip().split(';')
            airport = Airport(
                airport_data[0], airport_data[1], airport_data[2], airport_data[3],
                float(airport_data[4].replace(",", ".")), float(airport_data[5].replace(",", ".")),
                int(airport_data[6])
            )
            airports[airport_data[3]] = airport
    return airports

def read_flights(file_path: str) -> List[Flight]:
    """
    Reads flight data from a CSV file and returns a list of Flight objects.

    Parameters:
    file_path (str): The path to the CSV file containing flight data.

    Returns:
    List[Flight]: A list of Flight objects.
    """
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            flight_data = line.strip().split(';')

            origin_lat = airports[flight_data[0]].latitude
            origin_lon = airports[flight_data[0]].longitude
            destination_lat = airports[flight_data[2]].latitude
            destination_lon = airports[flight_data[2]].longitude

            distance = haversine((origin_lat, origin_lon), (destination_lat, destination_lon))

            flight = Flight(
                flight_data[0], flight_data[1], flight_data[2], flight_data[3],
                flight_data[4], flight_data[5], flight_data[6], int(flight_data[7]), distance
            )
            flights.append(flight)
    return flights

def haversine(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """
    Calculates the great-circle distance between two points on the Earth's surface.

    Parameters:
    coord1 (Tuple[float, float]): The latitude and longitude of the first point.
    coord2 (Tuple[float, float]): The latitude and longitude of the second point.

    Returns:
    float: The distance between the two points in kilometers.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371  # Radius of the Earth in kilometers

    return c * r

def find_nearest_airport(lat: float, lon: float) -> Airport:
    """
    Finds the nearest airport within a 30 km radius of the given coordinates.

    Parameters:
    lat (float): The latitude of the point.
    lon (float): The longitude of the point.

    Returns:
    Airport: The nearest Airport object or None if no airport is within 30 km.
    """
    nearest_airport = None
    nearest_distance = float('inf')

    for airport in airports.values():
        distance = haversine((lat, lon), (airport.latitude, airport.longitude))
        if distance < nearest_distance and distance <= 30:
            nearest_distance = distance
            nearest_airport = airport

    return nearest_airport

def build_graphs() -> None:
    """
    Builds the graphs for commercial, military, cargo, and general aviation flights.
    """
    for airport in airports.keys():
        commercial_digraph.add_vertex(airport)
        commercial_graph.add_vertex(airport)
        military_digraph.add_vertex(airport)
        military_graph.add_vertex(airport)
        cargo_digraph.add_vertex(airport)
        cargo_graph.add_vertex(airport)
        general_digraph.add_vertex(airport)
        general_graph.add_vertex(airport)

    for flight in flights:
        if flight.flight_type == "AVIACION_COMERCIAL":
            if flight.origin not in commercial_digraph.get_vertices():
                commercial_digraph.add_vertex(flight.origin)
                commercial_graph.add_vertex(flight.origin)
            if flight.destination not in commercial_digraph.get_vertices():
                commercial_digraph.add_vertex(flight.destination)
                commercial_graph.add_vertex(flight.destination)

            commercial_digraph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)
            commercial_graph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)

        elif flight.flight_type == "MILITAR" and flight.traffic == "N":
            if flight.origin not in military_digraph.get_vertices():
                military_digraph.add_vertex(flight.origin)
                military_graph.add_vertex(flight.origin)
            if flight.destination not in military_digraph.get_vertices():
                military_digraph.add_vertex(flight.destination)
                military_graph.add_vertex(flight.destination)

            military_digraph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)
            military_graph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)

        elif flight.flight_type == "AVIACION_CARGA":
            if flight.origin not in cargo_digraph.get_vertices():
                cargo_digraph.add_vertex(flight.origin)
                cargo_graph.add_vertex(flight.origin)
            if flight.destination not in cargo_digraph.get_vertices():
                cargo_digraph.add_vertex(flight.destination)
                cargo_graph.add_vertex(flight.destination)

            cargo_digraph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)
            cargo_graph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)

        elif flight.flight_type == "General":
            if flight.origin not in general_digraph.get_vertices():
                general_digraph.add_vertex(flight.origin)
                general_graph.add_vertex(flight.origin)
            if flight.destination not in general_digraph.get_vertices():
                general_digraph.add_vertex(flight.destination)
                general_graph.add_vertex(flight.destination)

            general_digraph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)
            general_graph.add_edge(flight.origin, flight.destination, flight.flight_distance, flight.flight_duration)

def get_airports_degree(graph: Graph) -> Dict[int, List[str]]:
    """
    Gets the degree of each airport in the given graph.

    Parameters:
    graph (Graph): The graph to analyze.

    Returns:
    Dict[int, List[str]]: A dictionary with degrees as keys and lists of airport ICAO codes as values.
    """
    degrees = {}
    for vertex in graph.get_vertices():
        degree = graph.get_degree(vertex)
        if degree not in degrees:
            degrees[degree] = []
        degrees[degree].append(vertex)
    return degrees

def find_path(origin_lat: float, origin_lon: float, destination_lat: float, destination_lon: float) -> Tuple[List[Tuple[str, str, str, str, float, float, float, float]], float, float]:
    """
    Finds a basic route from the origin to the destination using the commercial digraph.

    Parameters:
    origin_lat (float): The latitude of the origin.
    origin_lon (float): The longitude of the origin.
    destination_lat (float): The latitude of the destination.
    destination_lon (float): The longitude of the destination.

    Returns:
    Tuple[List[Tuple[str, str, str, str, float, float, float, float]], float, float]: The path information, total distance, and total time.
    """
    origin_airport = find_nearest_airport(origin_lat, origin_lon)
    destination_airport = find_nearest_airport(destination_lat, destination_lon)

    if origin_airport is None or destination_airport is None:
        return [], 0, 0
    else:
        path = commercial_digraph.bfs_path(origin_airport.icao, destination_airport.icao)
        path_info = []

        total_time = 0
        total_distance = 0

        for node in path:
            airport = node[0]

            total_distance += node[1][0]
            total_time += node[1][1]

            path_info.append((airports[airport].icao, airports[airport].name, airports[airport].city, airports[airport].country, node[1][0], node[1][1], total_distance, total_time))

        return path_info, total_distance, total_time

def find_max_degree(graph: Graph) -> Tuple[str, int]:
    """
    Finds the airport with the maximum degree in the given graph.

    Parameters:
    graph (Graph): The graph to analyze.

    Returns:
    Tuple[str, int]: The ICAO code of the airport with the maximum degree and the degree.
    """
    max_degree = 0
    max_degree_airport = None
    for vertex in graph.get_vertices():
        degree = graph.get_degree(vertex)
        if degree > max_degree:
            max_degree = degree
            max_degree_airport = vertex
    return max_degree_airport, max_degree

def find_mst(graph_type: str) -> Tuple[List[List[Tuple[str, Tuple[float, float]]]], Airport, int, float, int, float]:
    """
    Finds the most connected airport and its minimum spanning tree for a given graph type.

    Parameters:
    graph_type (str): The type of graph ("commercial", "military", "cargo").

    Returns:
    Tuple[List[List[Tuple[str, Tuple[float, float]]]], Airport, int, float, int, float]: The branches of the MST, the most connected airport, its degree, total distance, total segments, and total time.
    """
    if graph_type == "commercial":
        airport, degree = find_max_degree(commercial_graph)
        mst, distance, time = commercial_graph.prim(airport)
    elif graph_type == "military":
        airport, degree = find_max_degree(military_graph)
        mst, distance, time = military_graph.prim(airport)
    elif graph_type == "cargo":
        airport, degree = find_max_degree(cargo_graph)
        mst, distance, time = cargo_graph.prim(airport)

    branches = mst.find_branches(airport)

    return branches, airports[airport], degree, distance, len(branches), time

def top_n_mst(top: int) -> Tuple[str, int, List[List[Tuple[str, Tuple[float, float]]]], float, float]:
    """
    Finds the top N airports in Colombia by degree and builds an MST.

    Parameters:
    top (int): The number of top airports to consider.

    Returns:
    Tuple[str, int, List[List[Tuple[str, Tuple[float, float]]]], float, float]: The ICAO code, degree, MST branches, total distance, and total time.
    """
    degreeMap = get_airports_degree(commercial_digraph)
    degree_commercial_sorted = sorted(degreeMap.keys(), reverse=True)

    top_n_airports = []

    for degree in degree_commercial_sorted:
        if len(top_n_airports) >= top:
            break
        if isinstance(degreeMap[degree], list):
            for airport in degreeMap[degree]:
                if len(top_n_airports) >= top:
                    break
                airport_info = airports[airport]
                if airport_info.country == "Colombia":
                    top_n_airports.append((airport_info.name, airport_info.icao, airport_info.city, degree))
        else:
            airport_info = airports[degreeMap[degree]]
            top_n_airports.append((airport_info.name, airport_info.icao, airport_info.city, degree))

    graph = Graph()

    for airport_info in top_n_airports:
        for flight in flights:
            if flight.origin == airport_info[1]:
                for airport_info2 in top_n_airports:
                    if flight.destination == airport_info2[1]:
                        graph.add_edge(airport_info[1], airport_info2[1], flight.flight_distance, flight.flight_duration)

    mst, distance, time = graph.prim(top_n_airports[0][1])
    branches = mst.find_branches(top_n_airports[0][1])

    return top_n_airports[0][1], graph.get_degree(top_n_airports[0][1]), branches, distance, time

def shortest_path(origin_lat: float, origin_lon: float, destination_lat: float, destination_lon: float) -> Tuple[List[Tuple[str, str, float, float, float, float]], float, float]:
    """
    Finds the shortest path from the origin to the destination using Dijkstra's algorithm.

    Parameters:
    origin_lat (float): The latitude of the origin.
    origin_lon (float): The longitude of the origin.
    destination_lat (float): The latitude of the destination.
    destination_lon (float): The longitude of the destination.

    Returns:
    Tuple[List[Tuple[str, str, float, float, float, float]], float, float]: The path information, total distance, and total time.
    """
    origin_airport = find_nearest_airport(origin_lat, origin_lon)
    destination_airport = find_nearest_airport(destination_lat, destination_lon)

    if origin_airport is None or destination_airport is None:
        return [], 0, 0
    else:
        path = commercial_digraph.dijkstra(origin_airport.icao, destination_airport.icao)

        airports_info = path[0]
        weights = path[1]

        path_info = []

        distance = 0
        time = 0

        for i in range(len(airports_info) - 1):
            edge = [
                airports_info[i],
                airports_info[i + 1],
                weights[i][0],
                weights[i][1],
                distance + weights[i][0],
                time + weights[i][1]
            ]
            distance += weights[i][0]
            time += weights[i][1]

            path_info.append(edge)

        return path_info, distance, time
