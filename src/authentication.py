from flask import Blueprint, jsonify, request
import mysql.connector
import json

db = mysql.connector.connect(
    host='db',
    user='root',
    password='root',
    database='authentication'
)

auth_app = Blueprint("auth_app", __name__)


@auth_app.route('/user/<name>', methods=['GET'])
def get_user(name):
    cur = db.cursor()
    cur.execute("SELECT * FROM Users WHERE (user_name)=(%s)", [name])
    res = cur.fetchall()
    if len(res) == 0:
        return jsonify({'error': 'User does not exist.'}), 404
    user = res[0]
    data = {
        "code": 200,
        "id": user[0],
        "name": user[1],
        "gold": user[2],
        "diamond": user[3],
        "status": user[4]
    }
    return jsonify(data), 200


@auth_app.route('/signin', methods=['POST'])
def sign_in():
    cur = db.cursor()
    data = json.loads(request.data)
    uid, name, gold, diamond = data['userid'], data['username'], data['gold'], data['diamond']

    cur.execute("SELECT user_name FROM Users WHERE (user_id)=(%s)", [uid])
    res = cur.fetchall()

    if len(res) == 1:
        username = res[0][0]
        if name != username:
            return {"error_code": 404, "msg": "Another user with the same id already exists."}, 404

        cur.execute("SELECT quest_id FROM quest.user_quest_rewards WHERE user_id=(%s)", [uid])
        quests = cur.fetchall()
        if cur.rowcount < 1:
            return {"error_code": 404, "msg": "User is not working on a quest."}, 404

        qid = quests[0][0]
        cur.execute("UPDATE Users SET status=(%s) WHERE user_id=(%s)", ['not_new', uid])
        cur.execute("UPDATE quest.user_quest_rewards SET curr_streak=curr_streak+1 \
                              WHERE user_id=(%s) AND quest_id=(%s)", [uid, qid])
        cur.execute("SELECT curr_streak FROM quest.user_quest_rewards WHERE user_id=(%s)", [uid])
        streak = cur.fetchall()[0][0]
        if streak == 3:
            cur.execute("UPDATE quest.user_quest_rewards SET curr_streak=0, status=\"claimed\" \
                                  WHERE user_id=(%s) AND quest_id=(%s)", [uid, qid])
        msg = 'Welcome Back.'
    else:
        query1 = "INSERT INTO Users (user_id, user_name, gold, diamond, status) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query1, [uid, name, gold, diamond, 'new'])
        query2 = "INSERT INTO quest.user_quest_rewards (user_id, quest_id, status) VALUES (%s, %s, %s)"
        cur.execute(query2, [uid, 1, "not_claimed"])
        msg = 'New User successfully logged in.'
    db.commit()

    return jsonify({'message': msg}), 200
