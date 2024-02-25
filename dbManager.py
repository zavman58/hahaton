import json


class DBManager:
    def __init__(self, path):
        with open(path, 'r') as f:
            self.d = json.load(f)
            self.path = path
            self.max_id = self.d["max_id"]

    def close(self):
        with open(self.path, 'w') as f:
            json.dump(self.d, f)

    def __getitem__(self, item):
        if item not in list(self.d.keys()):
            return -1

        return self.d[item]

    def __setitem__(self, key, value):
        if key not in list(self.d.keys()):
            return -1

        self.d[key] = value

    def getall(self):
        return self.d

    def set_all(self, d):
        self.d = d

    def add_partner(self, partner_dict):
        partner_id = self.max_id + 1
        self.max_id = partner_id

        partner_dict["id"] = partner_id

        temp_d = self.getall()
        temp_d[partner_id] = partner_dict
        temp_d["max_id"] = self.max_id

        self.set_all(temp_d)

        return {"id": partner_dict["id"], "name": partner_dict["name"], "budget": partner_dict["budget"], "spent_budget": partner_dict["spent_budget"]}
