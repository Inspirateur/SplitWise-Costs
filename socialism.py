from collections import defaultdict
import json
import operator
from costs import compute_individual_costs


def load_data(costs_path, budget_path, gift_path=None):
    costs = compute_individual_costs(costs_path)
    # ensures that the name match between the budget and cost file
    with open(budget_path, "r", encoding="utf-8") as fbudget:
        budgets = json.load(fbudget)
    keydiff = budgets.keys() - costs.keys()
    if len(keydiff) > 0:
        raise ValueError(f"These names are in the budget file but not in the cost file:\n{', '.join(keydiff)}")
    # those not present in the budget have a budget equal to their cost
    budgets = costs | budgets
    # ensures that total budget > total cost
    margin = sum(budgets.values()) - sum(costs.values())
    if margin < 0:
        raise ValueError(f"The event costs {-margin} more than there is budget for.")
    gifts = {}
    if gift_path:
        # ensures that the name match between the gift and cost file
        with open(gift_path, "r", encoding="utf-8") as fgift:
            gifts = json.load(fgift)
        keydiff = gifts.keys() - costs.keys()
        if len(keydiff) > 0:
            raise ValueError(f"These names are in the gift file but not in the cost file:\n{', '.join(keydiff)}")
    return costs, budgets, gifts


def share(accounts: dict, amount, mask=None):
    # share an amount equally between accounts not present in mask
    if mask is None:
        mask = set()
    beneficiaries = accounts.keys() - mask
    diff = defaultdict(float)
    part = amount/len(beneficiaries)
    for beneficiary in beneficiaries:
        accounts[beneficiary] += part
        diff[beneficiary] += part
    return diff


def op_accounts(main, extra, op):
    for person, amount in extra.items():
        main[person] = op(main[person], amount)


def get_negatives(costs, budgets):
    return {person for person in costs if costs[person] > budgets[person]}


def compute_socialism(costs_path, budget_path, gift_path=None):
    costs, budgets, gifts = load_data(costs_path, budget_path, gift_path)
    # the amounts to be redistributed
    res = {person: 0 for person in costs}
    # Use gifts to reduce everyone's costs at the expense of the gifter
    for gifter, amount in gifts.items():
        costs[gifter] += amount
        res[gifter] -= amount
        diff = share(costs, -amount)
        op_accounts(res, diff, operator.sub)
    # compute the balance
    balance = {person: budgets[person]-costs[person] for person in costs}
    negs = dict(filter(lambda kv: kv[1] < 0, balance.items()))
    while len(negs) > 0:
        # set the negatives to exactly their budget
        op_accounts(costs, negs, operator.add)
        op_accounts(res, negs, operator.sub)
        # compute the total taken out of negatives this iteration
        to_share = -sum(negs.values())
        # share it among those who can
        diff = share(costs, to_share, negs.keys())
        op_accounts(res, diff, operator.sub)
        # compute the new balance
        balance = {person: budgets[person] - costs[person] for person in costs}
        negs = dict(filter(lambda kv: kv[1] < 0, balance.items()))
    return res


def display_socialism(costs_path, budget_path, gift_path=None):
    socialism = compute_socialism(costs_path, budget_path, gift_path)
    for person, v in socialism.items():
        print(person, f"{v:.2f}")


if __name__ == "__main__":
    display_socialism("nouvel-an-2021-2022_2022-01-10_export.csv", "budgets.json", "gifts.json")
