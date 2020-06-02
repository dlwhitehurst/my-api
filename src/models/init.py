import os
import json
import mysql.connector

##
# Initialize database
##
def initialize(http, db):
  # Create database of not exist
  cur, con = db.createDB()

  # Token
  token = http.auth.createtoken({
    'id': 1,
    'exp': {
      'days': 60
    }
  }, 'secret')

  path = os.path.dirname(os.path.realpath(__file__))

  try:
    for name in db.config['schema'].values():
      f=open(f'{path}/schema/{name}.sql', 'r')
      if f.mode == 'r':
        try:
          cur.execute(str(f.read()))
          print(f"Successfully created table '{name}'")
        except mysql.connector.Error as e:
          if e.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
            print(f'Table {name} already is exists.')
          else:
            print(e.msg)

    # Initial Person
    db.create('persons', {
      "id": 1,
      "firstname": "Tom",
      "lastname": "Smith",
      "dateofbirth": "06/01/2020",
      "gender": "M",
      "title": "Friend",
      "phonemobile": "123-456-7890",
      "phonehome": "919-456-1000",
      "phonework": "800-784-7890",
      "emailhome": "tsmith@gmail.com",
      "emailwork": "tsmith@acme.com",
      "auth": json.dumps({
        "key": "secret",
        "token": token
      })
    })

    # Initial address
    db.create('addresses', {
      "user": 1,
      "address1": "2932 Tram Road",
      "address2": "",
      "city": "Fuquay Varina",
      "state": "NC",
      "zipcode": "27526"
    })

  except mysql.connector.Error:
    pass

  cur.close()
  con.close()

  print('\nUse this token below for API Request:\n\n', f'{token}\n')

  return http.response({'success': 'Successfully initialized database'}, 201)
