from requests import get, post
post('http://localhost:8080/imalive/', data={'name': 'Jogador1'})
get('http://localhost:8080/start_game/')
post('http://localhost:8080/goto/', data={'direction': 1, 'distance': 2})
post('http://localhost:8080/goto/', data={'direction': 2, 'distance': 3})
post('http://localhost:8080/goto/', data={'direction': 3, 'distance': 4})
post('http://localhost:8080/goto/', data={'direction': 0, 'distance': 5})
