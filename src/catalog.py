from flask import Blueprint, request
import mysql.connector

db = mysql.connector.connect(
    host='db',
    user='root',
    password='root',
    port='3306',
    database='catalog'
)

cat_app = Blueprint("cat_app", __name__)


@cat_app.route('/quest_catalog', methods=['GET'])
def get_catalog():
    cur = db.cursor()
    cur.execute("SELECT * FROM Quests")
    res = cur.fetchall()
    quests = []
    for q in res:
        data = {
            "quest_id": q[0],
            "reward_id": q[1],
            "auto_claim": "True" if q[2] else "False",
            "streak": q[3],
            "duplication": q[4],
            "name": q[5],
            "description": q[6]
        }
        quests.append(data)
    return {'catalog': quests}, 200


@cat_app.route('/quest', methods=['GET'])
def get_quest():
    qid = request.json['quest_id']
    cur = db.cursor()
    cur.execute("SELECT * FROM catalog.Quests WHERE quest_id=(%s)", [qid])
    res = cur.fetchall()[0]
    data = {
        "quest_id": res[0],
        "reward_id": res[1],
        "auto_claim": "True" if res[2] else "False",
        "streak": res[3],
        "duplication": res[4],
        "name": res[5],
        "description": res[6]
    }
    return {"quest": data}, 200
