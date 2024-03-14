from flask import Blueprint, request
import mysql.connector

db = mysql.connector.connect(
    host='db',
    user='root',
    password='root',
    database='quest'
)

quest_app = Blueprint("quest_app", __name__)


@quest_app.route('/progress', methods=['GET'])
def get_quest_progress():
    qid = request.args.get('qid')
    uid = request.args.get('uid')
    cur = db.cursor()
    cur.execute("SELECT * FROM user_quest_rewards WHERE user_id=(%s) AND quest_id=(%s)", [uid, qid])
    res = cur.fetchall()
    if len(res) == 0:
        return {"error_code": 404, "error_msg": "No such quest in progress."}, 404
    res = res[0]
    data = {
        "user_id": res[0],
        "quest_id": res[1],
        "status": res[2],
        "date": res[3],
    }
    return {"progress": data}, 200
