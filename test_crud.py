import json
from collections import defaultdict

import requests


def test_list_albums():
    expected_status_code = 200
    expected_data_type = list
    expected_elements_amount = 100
    response = requests.get("https://jsonplaceholder.typicode.com/albums")
    res_data = json.loads(response.text)

    assert response.status_code == expected_status_code, \
        "Unexpected response status code. Current response {0}".format(response.status_code)

    assert type(res_data) == expected_data_type, \
        "Unexpected data type. Current data {0}, should be a {1}." \
        "".format(type(res_data), expected_data_type)

    assert len(res_data) == expected_elements_amount,\
        "Unexpected amount of elements. Current amount {0}, should be {1}." \
        "".format(len(res_data), expected_elements_amount)


def test_get_album():
    expected_status_code = 200
    expected_keys = sorted(['userId', 'id', 'title'])
    expected_data_type = dict

    response = requests.get("https://jsonplaceholder.typicode.com/albums/1")
    res_data = json.loads(response.text)
    res_keys = sorted(list(res_data.keys()))

    assert response.status_code == expected_status_code, \
        "Unexpected response status code. Current response {0}".format(response.status_code)

    assert type(res_data) == expected_data_type, \
        "Unexpected data type. Current data {0}, should be a {1}." \
        "".format(type(res_data), expected_data_type)

    assert res_keys == expected_keys, \
        "Request return unexpected data. Current data {0}, should be {1}" \
        "".format(res_keys, expected_keys)


def test_create_album():
    expected_status_code = 201

    data = {
        'userId': 1,
        'title': "I'm a new album",
    }
    response = requests.post(
        url="https://jsonplaceholder.typicode.com/albums",
        data=data,
    )
    res_data = defaultdict(lambda: "None")
    res_data.update(json.loads(response.text))

    assert response.status_code == expected_status_code,\
        "Unexpected response status code. Current response {0}".format(response.status_code)

    assert str(res_data['userId']) == str(data['userId']) and res_data['title'] == data['title'], \
        "Incorrect data for new album. Current data {0}, should be {1}." \
        "".format((str(res_data['userId']), res_data['title']), (str(data['userId']), data['title']))


def test_update_album():
    expected_status_code = 200
    data = {
        "userId": 142,
        "title": "New album title",
        "id": 500
    }
    init_response = requests.get("https://jsonplaceholder.typicode.com/albums/5")
    init_data = json.loads(init_response.text)
    response = requests.put(
        url="https://jsonplaceholder.typicode.com/albums/5",
        data=data,
    )
    res_data = defaultdict(lambda: "None")
    res_data.update(json.loads(response.text))

    assert response.status_code == expected_status_code, \
        "Unexpected response status code. Current response {0}".format(response.status_code)

    assert str(res_data["userId"]) == str(data["userId"]) and res_data["title"] == data["title"], \
        "Incorrect updated data. Current data {0}, should be {1}." \
        "".format((str(res_data['userId']), res_data['title']), (str(data['userId']), data['title']))

    assert res_data["title"] != init_data["title"] and str(res_data["userId"]) != str(init_data["userId"]),\
        "Incorrect changed data. Current data {0}, should be {1}." \
        "".format((str(res_data['userId']), res_data['title']), (str(init_data['userId']), init_data['title']))

    assert res_data["id"] == init_data["id"], \
        "An album id was changed but shouldn't. Current id {0}, expected {1}" \
        "".format(res_data["id"], init_data["id"])


def test_patch_album_title():
    expected_status_code = 200
    init_response = requests.get("https://jsonplaceholder.typicode.com/albums/5")
    init_data = json.loads(init_response.text)
    data = {
        "title": "I'm a new title! Yo-ho-ho",
    }
    response = requests.patch(
        url="https://jsonplaceholder.typicode.com/albums/5",
        data=data,
    )
    res_data = json.loads(response.text)
    assert response.status_code == expected_status_code,\
        "Unexpected response status code. Current response {0}".format(response.status_code)

    assert res_data["title"] == data["title"],\
        "Unexpected patched 'title'. Get {0}, expect {1}".format(res_data["title"], data["title"])

    assert res_data["title"] != init_data["title"], "'title' wasn't patched."
    assert res_data["userId"] == init_data["userId"], "'userId' was changed but shouldn't"
    assert res_data["id"] == init_data["id"], "'id' was changed but shouldn't"


def test_patch_album_userid():
    expected_status_code = 200
    data = {
        "userId": 666,
    }
    init_response = requests.get("https://jsonplaceholder.typicode.com/albums/6")
    init_data = json.loads(init_response.text)
    response = requests.patch(
        url="https://jsonplaceholder.typicode.com/albums/6",
        data=data,
    )
    res_data = defaultdict(lambda: "None")
    res_data.update(json.loads(response.text))

    assert response.status_code == expected_status_code, \
        "Unexpected response status code. Current response {0}".format(response.status_code)

    assert str(res_data["userId"]) == str(data["userId"]), \
        "Unexpected patched 'userId'. Get {0}, expect {1}".format(res_data["userId"], data["userId"])

    assert res_data["userId"] != init_data["userId"], "'userId' wasn't patched"
    assert res_data["title"] == init_data["title"], "'title' was changed but shouldn't."
    assert res_data["id"] == init_data["id"], "'id' was changed but shouldn't"


def test_delete_album():
    expected_del_response = 200
    expected_get_response = 404

    del_response = requests.delete("https://jsonplaceholder.typicode.com/albums/7")
    assert del_response.status_code == expected_del_response, "Deleting is unsuccessful"
    get_response = requests.get("https://jsonplaceholder.typicode.com/albums/7")
    assert get_response.status_code == expected_get_response, "The resource was not deleted"
