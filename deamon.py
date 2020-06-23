import time
import datetime
import psycopg2.extras

connection = psycopg2.connect(user='pptxkiqjrrvkex',
                              password='1edf1b8df37cc3ad25ec72eac0d5e933472d6466fb38564bdc0205dfbbc60041',
                              host="ec2-54-247-89-181.eu-west-1.compute.amazonaws.com",
                              port="5432",
                              database='d896g2bfugmqi2')
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

while True:

    now = datetime.datetime.now()
    cursor.execute('select * from messanger where status=False and n < 5 and datetime <= %s',
                   (now,))
    messages = cursor.fetchall()
    for message in messages:
        if message is not None:
            cursor.execute('update messanger set status=%s where id=%s', (True, message['id']))
            connection.commit()
    time.sleep(5)
