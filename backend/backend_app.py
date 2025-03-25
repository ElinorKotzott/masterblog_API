from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

posts = [
    {'id': 1, 'title': 'First post', 'content': 'This is the first post.'},
    {'id': 2, 'title': 'Second post', 'content': 'This is the second post.'},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':

        new_post = request.get_json()


        if new_post['title'] and new_post['content']:
            new_id = max(post['id'] for post in posts) + 1
            new_post['id'] = new_id

            posts.append(new_post)

            return jsonify(new_post), 201

        elif not new_post['title'] and not new_post['content']:
            return jsonify({'error': 'please provide title and content!'}), 400

        elif not new_post['title']:
            return jsonify({'error': 'please provide a title'}), 400

        elif not new_post['content']:
            return jsonify({'error': 'please provide the content!'}), 400


    else:
        return jsonify(posts)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    to_delete = next((post for post in posts if post['id'] == id), None)
    if to_delete is None:
        return jsonify({"error": "This ID doesn't exist!"}), 404
    else:
        posts.remove(to_delete), 200





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
