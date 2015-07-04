from bottle import route, run, request
from pickle import load, dump

db_file = 'players.db'
action_file = 'actions.db'

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

def write_action(action):
    print(action)
    with(open(action_file, 'a')) as actions:
        actions.write(action)

@route('/goto/', method='POST')
def goto():
  direction = request.POST.get('direction')
  distance = request.POST.get('distance')
  write_action('goto:{}:{}:{}\n'.format(request.remote_addr, direction, distance))

@route('/shoot/', method='POST')
def shoot():
  direction = request.POST.get('direction')
  write_action('shoot:{}:{}\n'.format(request.remote_addr, direction))

@route('/get_players/')
def get_players():
    return players

@route('/imalive/', method='POST')
def im_alive():
    name = request.POST.get('name')
    players[request.remote_addr] = {'name': name}
    dump_db(players)
    write_action('add_player:{}:{}\n'.format(request.remote_addr, name))

@route('/start_game/')
def start_game():
    write_action('STARTGAME\n')
run(host='0.0.0.0', port=8080, debug=True, reloader=True)
