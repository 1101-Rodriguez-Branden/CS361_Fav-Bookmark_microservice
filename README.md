# Favorites/Bookmarks Microservice

# Description
The Favorites / Bookmarks Microservice allows another program to add, view, and remove saved favorite items. This microservice is intentionally general so it can work with many different main programs. A favorite item could be a pet, product, recipe, article, listing, image, or any other type of item. The microservice uses a REST API and stores favorite items in a local JSON file named "favorites.json".

# Communication Contract

1. We will communicate via Discord.
2. We expect a response within 24 hours.
3. We will implement a backup plan after 72 hours of unresponsiveness. The response will be divided amongst the rest of the team.
4. Treat each other with respect. Treat each other how you want to be treated.
5. Provide constructive criticism when necessary. It's important to provide feedback to make the project better overall. Feedback is constructive and called for, not disrespectful or rude.

# Communication Pipe

This microservice uses a REST API.

# Base URL
http://127.0.0.1:5004

# Data Format
All requests and responses use JSON.

# How to Run the Microservice

Install the required dependencies:
pip install -r requirements.txt

Start the microservice:
python3 app.py

The microservice will run locally at:
http://127.0.0.1:5004

# How to Programmatically REQUEST Data

Other programs can request data from the microservice by sending HTTP requests to /favorites.

The microservice supports three main actions:

1. Add a favorite
2. View a user's favorites
3. Remove a favorite

# Example Python Request

```python
import requests

favorite = {
    "user_id": "123",
    "item_id": "cat_7",
    "item_type": "pet",
    "name": "Fred"
}

response = requests.post(
    "http://127.0.0.1:5004/favorites",
    json=favorite
)

print(response.status_code)
print(response.json())
```

# How to Programmatically RECEIVE Data

The requesting program receives data from the microservice as JSON. The response depends on which endpoint is called.

# Example Response: Add Favorite

# Status Code
201 Created

# JSON Response

```json
{
  "message": "Favorite added successfully",
  "favorite": {
    "user_id": "123",
    "item_id": "cat_7",
    "item_type": "pet",
    "name": "Fred",
    "saved_date": "2026-05-18"
  }
}
```

# Test Program

This repository includes a test program named:
test_client.py

The test program demonstrates that another program can call the microservice and receive data back. To run the test program, first start the microservice in one terminal:

python3 app.py

Then, in a second terminal, run:

python3 test_client.py

The test program performs these actions:

1. Sends a `POST` request to add a favorite
2. Sends a `GET` request to view favorites for a user
3. Sends an invalid `POST` request to test error handling
4. Sends a `DELETE` request to remove a favorite
5. Sends another `GET` request to confirm the favorite was removed

# UML Sequence Diagram

# Notes

The `favorites.json` file may be empty after running the test program because the test program adds a favorite and then removes it.

An empty `favorites.json` file should look like this:

```json
[]
```