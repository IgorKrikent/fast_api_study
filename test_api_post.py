from pprint import pprint

import storage


# import requests
#
# headers = {
#     'accept': 'application/json',
#     'Content-Type': 'application/json',
# }
#
# json_data = {
#     'title': 'Some Movie',
#     'genres': [],
#     'created_by': {
#         'director': [
#             'Frank Miller',
#             'Quentin Tarantino',
#         ],
#         'producer': [
#             'Jason Bloom',
#             'George Lucas',
#         ],
#         'scriptwriter': [
#             'M. Night Shyamalan',
#             'Christopher Nolan',
#         ],
#     },
#     'cast': [
#         'string',
#     ],
#     'duration': 2,
#     'description': 'string',
#     'tags': [],
#     'rating': 0,
#     'votes': 0,
#     'poster': '',
# }
#
# response = requests.post('http://127.0.0.1:9010/api/films/post/', headers=headers, json=json_data)

def test_create_film(client):

    json_data = {
        'title': 'Some Movie',
        'genres': [],
        'created_by': {
            'director': [
                'Frank Miller',
                'Quentin Tarantino',
            ],
            'producer': [
                'Jason Bloom',
                'George Lucas',
            ],
            'scriptwriter': [
                'M. Night Shyamalan',
                'Christopher Nolan',
            ],
        },
        'cast': [
            'string',
        ],
        'duration': 2,
        'description': 'string',
        'tags': [],
        'rating': 0,
        'votes': 0,
        'poster': '',
    }

    response = client.post('/api/films/post/', json=json_data)

    pprint(response.json())
    saved_film = storage.storage.get_film(film_id=response.json()['uuid'])

    assert saved_film
