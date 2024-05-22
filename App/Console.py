from Logic import *;
from tabulate import tabulate

airports = {}
flights = []

def print_menu():
    print("\nMenú:")
    print("0. Charge Data")
    print("1. Req 1")
    print("2. Req 2")
    print("3. Req 3")
    print("4. Req 4")
    print("5. Req 5")
    print("6. Req 6")
    print("7. Req 7")
    print("8. Exit")


def charge_data():
    airports = read_airports("Data/airports-2022.csv")
    flights = read_flights("Data/fligths-2022.csv")


    build_graphs()

    # AUXILIAR

    def get_top_5_airports(degreed_sorted: list, airports: dict, degreeMap: dict) -> list:

        top_5_strings = []

        for degree in degreed_sorted:
            if len(top_5_strings) >= 5:
                break
            if isinstance(degreeMap[degree], list):
                for airport in degreeMap[degree]:
                    if len(top_5_strings) >= 5:
                        break
                    airport_info = airports[airport]
                    top_5_strings.append((airport_info.name, airport_info.icao, airport_info.city, degree))
            else:
                airport_info = airports[airport]
                top_5_strings.append((airport_info.name, airport_info.icao, airport_info.city, degree))

        return top_5_strings
    
    def get_bottom_5_airports(degreed_sorted: list, airports: dict, degreeMap: dict) -> list:

        bottom_5_strings = []

        for degree in reversed(degreed_sorted):
            if len(bottom_5_strings) >= 5:
                break
            if isinstance(degreeMap[degree], list):
                for airport in degreeMap[degree]:
                    if len(bottom_5_strings) >= 5:
                        break
                    airport_info = airports[airport]
                    bottom_5_strings.append((airport_info.name, airport_info.icao, airport_info.city, degree))
            else:
                airport_info = airports[degreeMap[degree]]
                bottom_5_strings.append((airport_info.name, airport_info.icao, airport_info.city, degree))

        return bottom_5_strings

    def print_table_charge(data, headers):
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print("\n" + "-"*40 + "\n")

    #PRINTS

    print(f'Total airports charged: {len(airports.keys())}')
    print(f'Total flights charged: {len(flights)}')

    #TOTAL

    degree_general = get_airports_degree(general_digraph)
    degree_general_sorted = sorted(degree_general.keys(), reverse=True)

    top_5_general = get_top_5_airports(degree_general_sorted, airports, degree_general)
    bottom_5_general = get_bottom_5_airports(degree_general_sorted, airports, degree_general)

    print("\n#################################################################")
    print("Top 5 most concurrent airports:")
    print("###################################################################\n")
    print_table_charge(top_5_general, ["Name", "ICAO", "City", "Degree"])
    print("\n#################################################################")
    print("Top 5 least concurrent airports:")
    print("###################################################################\n")
    print_table_charge(bottom_5_general, ["Name", "ICAO", "City", "Degree"])

    #COMMERICAL

    degree_commercial = get_airports_degree(commercial_digraph)
    degree_commercial_sorted = sorted(degree_commercial.keys(), reverse=True)

    top_5_commercial = get_top_5_airports(degree_commercial_sorted, airports, degree_commercial)
    bottom_5_commercial = get_bottom_5_airports(degree_commercial_sorted, airports, degree_commercial)

    print("\n#################################################################")
    print("Top 5 most concurrent commercial airports:")
    print("###################################################################\n")
    print_table_charge(top_5_commercial, ["Name", "ICAO", "City", "Degree"])
    print("\n#################################################################")
    print("Top 5 least concurrent commercial airports:")
    print("###################################################################\n")
    print_table_charge(bottom_5_commercial, ["Name", "ICAO", "City", "Degree"])

    #MILITAR

    degree_military = get_airports_degree(military_digraph)
    degree_military_sorted = sorted(degree_military.keys(), reverse=True)

    top_5_military = get_top_5_airports(degree_military_sorted, airports, degree_military)
    bottom_5_military = get_bottom_5_airports(degree_military_sorted, airports, degree_military)

    print("\n#################################################################")
    print("Top 5 most concurrent military airports:")
    print("###################################################################\n")
    print_table_charge(top_5_military, ["Name", "ICAO", "City", "Degree"])
    print("\n#################################################################")
    print("Top 5 least concurrent military airports:")
    print("###################################################################\n")
    print_table_charge(bottom_5_military, ["Name", "ICAO", "City", "Degree"])

    #CARGO

    degree_cargo = get_airports_degree(cargo_digraph)
    degree_cargo_sorted = sorted(degree_cargo.keys(), reverse=True)

    top_5_cargo = get_top_5_airports(degree_cargo_sorted, airports, degree_cargo)
    bottom_5_cargo = get_bottom_5_airports(degree_cargo_sorted, airports, degree_cargo)

    print("\n#################################################################")
    print("Top 5 most concurrent cargo airports:")
    print("###################################################################\n")
    print_table_charge(top_5_cargo, ["Name", "ICAO", "City", "Degree"])
    print("\n#################################################################")
    print("Top 5 least concurrent cargo airports:")
    print("###################################################################\n")
    print_table_charge(bottom_5_cargo, ["Name", "ICAO", "City", "Degree"])


def print_path(path):
    print(tabulate(path, headers=["ICAO", "NAME", "CITY", "COUNTRY", "DISTANCE", "TIME", "TOTAL_DISTANCE", "TOTAL_TIME"], tablefmt="grid"))

def print_tree(mst):
   for i in range(len(mst)):
        path_l = []
        path_distance = 0
        path_time = 0
        for j in range(len(mst[i])):
                path = []
                if j == len(mst[i]) - 1:
                        break
                path.append(mst[i][j][0])
                path.append(mst[i][j+1][0])
                path.append(str(mst[i][j+1][1][0]))
                path.append(str(mst[i][j+1][1][1]))

                path_distance += int(mst[i][j+1][1][0])
                path_time += int(mst[i][j+1][1][1])

                path.append(str(path_distance))
                path.append(str(path_time))

                path_l.append(path)

        print("\n#################################################################")
        print(f"Path {i+1}:")
        print("###################################################################\n")
                
        print(tabulate(path_l, headers=["DEPARTURE_ICAO", "ARRIVAL_ICAO", "DISTANCE", "TIME", "TOTAL_DISTANCE", "TOTAL_TIME"], tablefmt="grid"))

def print_dijkstra(path):

    print(tabulate(path, headers=["DEPARTURE_ICAO", "ARRIVAL_ICAO", "DISTANCE", "TIME", "TOTAL_DISTANCE", "TOTAL_TIME"], tablefmt="grid"))

    

def main():
    while True:
        print_menu()
        option = input("Select an option: ")

        if option == "0":
            charge_data()
        elif option == "1":
            lat1 = float(input("Enter the latitude of the origin: ").replace(",", "."))
            lon1 = float(input("Enter the longitude of the origin: ").replace(",", "."))
            lat2 = float(input("Enter the latitude of the destination: ").replace(",", "."))
            lon2 = float(input("Enter the longitude of the destination: ").replace(",", "."))

            path, distance, time = find_path(lat1, lon1, lat2, lon2)
            print("\n#################################################################")
            if len(path) == 0:
                print("No path was found.")
            else:
                print(f"Path from {path[0][1]} to {path[-1][1]}:")
                print(f'Time: {time} minutes')
                print(f'Distance: {distance} km')
                print(f'Num of stops: {len(path) - 1}')
            print("###################################################################\n")
            print_path(path)
        elif option == "2":
            lat1 = float(input("Enter the latitude of the origin: ").replace(",", "."))
            lon1 = float(input("Enter the longitude of the origin: ").replace(",", "."))
            lat2 = float(input("Enter the latitude of the destination: ").replace(",", "."))
            lon2 = float(input("Enter the longitude of the destination: ").replace(",", "."))

            path, distance, time = find_path(lat1, lon1, lat2, lon2)
            print("\n#################################################################")
            if len(path) == 0:
                print("No path was found.")
            else:
                print(f"Path from {path[0][1]} to {path[-1][1]}:")
                print(f'Time: {time} minutes')
                print(f'Distance: {distance} km')
                print(f'Num of stops: {len(path) - 1}')
            print("###################################################################\n")
            print_path(path)
        elif option == "3":
            mst, airport, degree, total_distance, total_trayects, time = find_mst("commercial")
            
            if len(mst) == 0:
                print("No path was found.")
            else:
                print_tree(mst)

                print("\n#################################################################")
                print(f'Most concurrent commercial airport: {airport.name} with {degree} flights')
                print(f'Total distance: {total_distance} km')
                print(f'Total trayects: {total_trayects}')
                print(f'Total time: {time} minutes')
                print("###################################################################\n")
        elif option == "4":
            mst, airport, degree, total_distance, total_trayects, time = find_mst("cargo")
            
            if len(mst) == 0:
                print("No path was found.")
            else:
                print_tree(mst)

                print("\n#################################################################")
                print(f'Most concurrent cargo airport: {airport.name} with {degree} flights')
                print(f'Total distance: {total_distance} km')
                print(f'Total trayects: {total_trayects}')
                print(f'Total time: {time} minutes')
                print("###################################################################\n")
        elif option == "5":
            mst, airport, degree, total_distance, total_trayects, time = find_mst("military")
            
            if len(mst) == 0:
                print("No path was found.")
            else:
                print_tree(mst)

                print("\n#################################################################")
                print(f'Most concurrent military airport: {airport.name} with {degree} flights')
                print(f'Total distance: {total_distance} km')
                print(f'Total trayects: {total_trayects}')
                print(f'Total time: {time} minutes')
                print("###################################################################\n")
        elif option == "6":
            top = int(input("Enter the top: "))
            icao, degree, mst, distance, time = top_n_mst(top)

            print("\n#################################################################")
            if len(mst) == 0:
                print("No path was found.")
            else:
                print(f'Most important airport: {icao} with {degree} flights')
                print(f'Total distance: {distance} km')
                print(f'Total time: {time} minutes')
            print("###################################################################\n")

            print_tree(mst)
        elif option == "7":
            lat1 = float(input("Enter the latitude of the origin: ").replace(",", "."))
            lon1 = float(input("Enter the longitude of the origin: ").replace(",", "."))
            lat2 = float(input("Enter the latitude of the destination: ").replace(",", "."))
            lon2 = float(input("Enter the longitude of the destination: ").replace(",", "."))

            path, total_distance, total_time = shortest_path(lat1, lon1, lat2, lon2)

            print("\n#################################################################")
            if len(path) == []:
                print("No path was found.")
            else:
                print(f'Shortest path from {path[0][0]} to {path[-1][1]}:')
                print(f'Total distance: {total_distance} km')
                print(f'Total time: {total_time} minutes')
                print(f'Num of stops: {len(path) - 1}')
            print("###################################################################\n")

            print_dijkstra(path)
        elif option == "10":
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")



if __name__ == "__main__":
    main()