from dbManager import DBManager
from script_get_preditcion import get_predict
import json, datetime
PATH='db.json'
PREDICTIONSFILE='predictions.json'


def main(command_id, dict_string, partner_id):
    command_id = int(command_id)
    
    dbm = DBManager(PATH)

    if dict_string != '':
        dict_string = json.loads(dict_string)
    
    if command_id == 0:
        return add_new(dict_string, dbm)
    elif command_id == 1:
        return find_partner(partner_id, dbm)
    elif command_id == 2:
        return update_partner(dict_string, partner_id, dbm)
    else:
        return f'OSHIBKA, id - {command_id}'


def add_new(dict_string, dbm):
    kent = {"name": dict_string['name'], "budget": dict_string['budget'], "spent_budget": 0.0, "is_stopped": 0, 'transactions': []}
    
    final_dict = dbm.add_partner(kent)

    dbm.close()

    get_predict(dict_string['name'], dict_string['budget'], final_dict["id"])
    
    return str(final_dict)


def find_partner(partner_id, dbm):
    partner_dict = dbm[partner_id]
    dbm.close()

    return {"id": partner_dict["id"], "name": partner_dict["name"], "budget": partner_dict["budget"],
            "spent_budget": partner_dict["spent_budget"], "is_stopped": partner_dict["is_stopped"]}


def update_partner(dict_string, partner_id, dbm):
    partner_dict = dbm[partner_id]

    if partner_dict == -1:
        return -1

    partner_dict["transactions"].append((dict_string["date"], dict_string["cashback"]))
    partner_dict["spent_budget"] += dict_string["cashback"]

    with open(PREDICTIONSFILE, 'r') as f:
        d = json.load(f)
        stop_time = d[str(partner_id)]

    partner_dict["is_stopped"] = int(datetime.datetime.fromisoformat(dict_string["date"]) >= datetime.datetime.fromisoformat(stop_time))

    dbm[partner_id] = partner_dict
    dbm.close()

    return '{}'
