from flask import Flask, jsonify,request
import psycopg2.extras
from datetime import datetime
from validation import Validator

connection = psycopg2.connect(user='pptxkiqjrrvkex',
                              password='1edf1b8df37cc3ad25ec72eac0d5e933472d6466fb38564bdc0205dfbbc60041',
                              host="ec2-54-247-89-181.eu-west-1.compute.amazonaws.com",
                              port="5432",
                              database='d896g2bfugmqi2')
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

app = Flask(__name__)


@app.route('/api/v1/message', methods=['POST'])
def save_message_db():
    message_data = request.get_json(force=True)
    validation_message = Validator()
    message_text = message_data['text']
    messengers = message_data['messangers']
    datetime_object = validation_message.date(message_data['datetime'])
    if datetime_object is None:
        return 'incorrect time format'
    data = []
    for messenger, phone in messengers.items():
        phone = validation_message.phone(phone)
        if phone is None:
            return 'incorrect phone number'
        data.append((messenger, message_text, datetime_object, phone, False, 0))
    sql = "insert into Messanger(messanger, text, datetime, phone, status,n) values (%s,%s,%s,%s,%s,%s)"
    cursor.executemany(sql, data)
    connection.commit()
    return 'ok'


@app.route('/api/v1/status', methods=['GET'])
def message_status():
    cursor.execute('select * from messanger')
    data = cursor.fetchall()
    result = {'response': []}
    for i in data:
        if i['status'] is False:
            result['response'].append({i['phone']: 'not sent'})
        else:
            result['response'].append({i['phone']: 'sent'})
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
