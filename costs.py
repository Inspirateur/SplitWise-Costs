import csv
from collections import defaultdict


def read_splitwise_csv(csv_path):
    with open(csv_path, "r", encoding="utf-8") as fcsv:
        csv_reader = csv.DictReader(fcsv)
        # the last row is the final balance
        rows = list(csv_reader)[:-1]
    return rows


def compute_individual_costs(csv_path):
    data = read_splitwise_csv(csv_path)
    costs = defaultdict(float)
    for row in data:
        cost = None
        for k, v in row.items():
            try:
                v = float(v)
                # we assume the first readable float is the total cost of the line
                if cost is None:
                    cost = v
                else:
                    # each float after that is the cost associated with the person k on this row
                    if v > 0:
                        costs[k] += cost - v
                    else:
                        costs[k] -= v
            except ValueError:
                pass
    return costs


def print_individual_costs(csv_path):
    costs = compute_individual_costs(csv_path)
    for person, cost in costs.items():
        print(person, f"{cost:.2f}")


if __name__ == "__main__":
    print_individual_costs("nouvel-an-2021-2022_2022-01-10_export.csv")
