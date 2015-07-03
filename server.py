from bottle import route, run, request
from pickle import load, dump

db_file = 'players.db'

def load_db():
    with open(db_file, 'rb') as db:
        return load(db)

def dump_db(obj):
    with open(db_file, 'wb') as db:
        return dump(obj, db)

try:
    players = load_db()
except:
    players = {}

@route('/goto/<direction>/<distance>/')
def goto(direction, distance):
  print(direction)
  print(distance)

@route('shoot')
def shoot(direction):
  pass

@route('/get_players/')
def get_players():
    return players

@route('/imalive/', method='POST')
def im_alive():
    players[request.remote_addr] = {'name':request.POST.get('name')}
    dump_db(players)

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
