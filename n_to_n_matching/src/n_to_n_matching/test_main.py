from n_to_n_matching.matcher import GjVolunteerAllocationGame


def test_1():
    #dates_input = Util.read_yaml_to_dict(base_url, "dates.yml")
    dates_input = [
        { "date": "2024-04-01", },
        {
            "date": "2024-04-08",
            "num_leader": 1,
            "num_commitee": 2,
            "num_general": 3,
        },
        { "date": "2024-04-15", },
        { "date": "2024-04-22", }
    ]
    #guardian_input = Util.read_yaml_to_dict(base_url, "guardian.yml")
    guardian_input = [
        {
            "id": 1,
            "name": "guardian-name1",
            "phone": "000-000-0000",
            "email": "1@dot.com.dummy",
            "children": {
              "child_id": 1111,
              "child_id": 1112},
            "role_id": 1
        },
        {
            "id": 2,
            "name": "guardian-name2",
            "phone": "000-000-0000",
            "email": "2@dot.com.dummy",
            "children": {
              "child_id": 1113},
            "role_id": 2
        },
        {
            "id": 3,
            "name": "guardian-name3",
            "phone": "000-000-0000",
            "email": "3@dot.com.dummy",
            "children": {
                "child_id": 1114,
                "child_id": 1115,
                "child_id": 1116},
            "role_id": 2
        },
        {
            "id": 4,
            "name": "guardian-name4",
            "phone": "000-000-0000",
            "email": "4@dot.com.dummy",
            "children": {
              "child_id": 1117},
            "role_id": 1
        },
        {
            "id": 5,
            "name": "guardian-name5",
            "phone": "000-000-0000",
            "email": "5@dot.com.dummy",
            "children": {
                "child_id": 1118,
                "child_id": 1119,
                "child_id": 1120,
                "child_id": 1121},
            "role_id": 2
        },
    ]

    num_dates = len(dates_input)
    num_guardians = len(guardian_input)
    game = GjVolunteerAllocationGame.create_from_dictionaries(
        dates_input, guardian_input)
    solution = game.solve()
    for date, guardians in solution.items():
        print(f"{date} ({date.capacity}): {guardians}")
    GjVolunteerAllocationGame.print_tabular(solution)

