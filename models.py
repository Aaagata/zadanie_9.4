import json

class Costs:
    def __init__(self):
        try:
            with open("costs.json", "r") as f:
                self.costs = json.load(f)
        except FileNotFoundError:
            self.costs = []

    def all(self):
        return self.costs

    def get(self, id):
        cost = [cost for cost in self.all() if cost['id'] == id]
        if cost:
            return cost[0]
        return []

    def create(self, data):
        self.costs.append(data)
        self.save_all()

    def save_all(self):
        with open("costs.json", "w") as f:
            json.dump(self.costs, f)

    def update(self, id, data):
        cost = self.get(id)
        if cost:
            index = self.costs.index(todo)
            self.costs[index] = data
            self.save_all()
            return True
        return False

    def delete(self, id):
        cost = self.get(id)
        if cost:
            self.costs.remove(cost)
            self.save_all()
            return True
        return False

costs = Costs()