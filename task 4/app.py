from flask import Flask, request, jsonify

app = Flask(__name__)
users = {}
next_user_id = 1 # To assign unique IDs to new users

@app.route('/')
def home():
    return "Welcome to the User API!"

# --- GET all users and GET a single user ---
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users.values())) # Return a list of all user dictionaries

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

# --- POST: Create a new user ---
@app.route('/users', methods=['POST'])
def create_user():
    global next_user_id
    data = request.get_json()

    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"message": "Name and email are required"}), 400

    new_user = {
        "id": next_user_id,
        "name": data['name'],
        "email": data['email']
    }
    users[next_user_id] = new_user
    next_user_id += 1
    return jsonify(new_user), 201 # 201 Created

# --- PUT: Update an existing user ---
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided for update"}), 400

    # Update only provided fields
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']

    return jsonify(user)

# --- DELETE: Delete a user ---
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    app.run(debug=True) 