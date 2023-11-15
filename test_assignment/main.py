from test_assignment.city_grid import CityGrid


def main():
    city = CityGrid(10, 10)
    towers = city.optimize_towers(3)
    path = city.find_most_reliable_path(3, towers, towers[0], towers[3])
    city.visualize_city(towers, path)


if __name__ == "__main__":
    main()