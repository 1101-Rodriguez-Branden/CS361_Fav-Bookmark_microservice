import requests

BASE_URL = "http://127.0.0.1:5004"


def print_response(title, response):
    print("\n" + title)
    print("Status code:", response.status_code)
    print("Response:")
    print(response.json())


def test_add_favorite():
    favorite = {
        "user_id": "123",
        "item_id": "cat_7",
        "item_type": "pet",
        "name": "Fred"
    }

    response = requests.post(
        BASE_URL + "/favorites",
        json=favorite
    )

    print_response("ADD FAVORITE TEST", response)


def test_get_favorites():
    response = requests.get(
        BASE_URL + "/favorites",
        params={"user_id": "123"}
    )

    print_response("GET FAVORITES TEST", response)


def test_remove_favorite():
    favorite_to_remove = {
        "user_id": "123",
        "item_id": "cat_7"
    }

    response = requests.delete(
        BASE_URL + "/favorites",
        json=favorite_to_remove
    )

    print_response("REMOVE FAVORITE TEST", response)


def test_invalid_request():
    bad_favorite = {
        "user_id": "123"
    }

    response = requests.post(
        BASE_URL + "/favorites",
        json=bad_favorite
    )

    print_response("INVALID REQUEST TEST", response)


def main():
    test_add_favorite()
    test_get_favorites()
    test_invalid_request()
    test_remove_favorite()
    test_get_favorites()


if __name__ == "__main__":
    main()