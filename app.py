from flask import Flask, request, jsonify
from datetime import date
import json
import os

app = Flask(__name__)

FAVORITES_FILE = "favorites.json"


# favorites .json exists before use
def make_file_if_missing():
    if not os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "w") as file:
            json.dump([], file)


# reads all favs from json
def read_favorites():
    make_file_if_missing()

    with open(FAVORITES_FILE, "r") as file:
        try:
            favorites = json.load(file)
        except json.JSONDecodeError:
            favorites = []

    return favorites


# save all favs back to json
def write_favorites(favorites):
    with open(FAVORITES_FILE, "w") as file:
        json.dump(favorites, file, indent=4)


# checks if a fav exists
def favorite_exists(favorites, user_id, item_id):
    for favorite in favorites:
        if favorite["user_id"] == user_id and favorite["item_id"] == item_id:
            return True
    return False


# gets specific favorite from favorites
def get_favorite(favorites, user_id, item_id):
    for favorite in favorites:
        if favorite["user_id"] == user_id and favorite["item_id"] == item_id:
            return favorite
    return None


# message to show its running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Favorites / Bookmarks Microservice is running."}), 200


# Add a fav
@app.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    user_id = data.get("user_id")
    item_id = data.get("item_id")
    item_type = data.get("item_type")
    name = data.get("name", "")

    if not user_id or not item_id or not item_type:
        return jsonify(
            {
                "error": "Missing required fields: user_id, item_id, and item_type are required"
            }
        ), 400

    favorites = read_favorites()

    # Check if this fav is already saved for user
    if favorite_exists(favorites, user_id, item_id):
        return jsonify(
            {
                "message": "Favorite already exists",
                "favorite": get_favorite(favorites, user_id, item_id),
            }
        ), 200

    new_favorite = {
        "user_id": user_id,
        "item_id": item_id,
        "item_type": item_type,
        "name": name,
        "saved_date": str(date.today()),
    }

    favorites.append(new_favorite)
    write_favorites(favorites)

    return jsonify(
        {"message": "Favorite added successfully", "favorite": new_favorite}
    ), 201


# gets all favs of a user
@app.route("/favorites", methods=["GET"])
def get_favorites():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing required parameter: user_id"}), 400

    favorites = read_favorites()

    user_favorites = []

    for favorite in favorites:
        if favorite["user_id"] == user_id:
            user_favorites.append(favorite)

    return jsonify({"user_id": user_id, "favorites": user_favorites}), 200


# Removes a fav
@app.route("/favorites", methods=["DELETE"])
def remove_favorite():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    user_id = data.get("user_id")
    item_id = data.get("item_id")

    if not user_id or not item_id:
        return jsonify(
            {"error": "Missing required fields: user_id and item_id are required"}
        ), 400

    favorites = read_favorites()

    new_favorites = []
    removed = False

    for favorite in favorites:
        if favorite["user_id"] == user_id and favorite["item_id"] == item_id:
            removed = True
        else:
            new_favorites.append(favorite)

    if not removed:
        return jsonify({"error": "Favorite not found"}), 404

    write_favorites(new_favorites)

    return jsonify({"message": "Favorite removed successfully"}), 200


if __name__ == "__main__":
    make_file_if_missing()
    app.run(host="127.0.0.1", port=5004, debug=True)
