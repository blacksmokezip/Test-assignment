from test_assignment.city_grid import CityGrid


def main() -> None:
    city = CityGrid(22, 30)
    towers = city.optimize_towers(5)
    path = city.find_most_reliable_path(5, towers, towers[2], towers[7])
    city.visualize_city(towers, path)


if __name__ == "__main__":
    main()