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


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def update_or_delete_post(post_id):
    if request.method=='DELETE':
        to_delete = next((post for post in posts if post['id'] == post_id), None)
        if to_delete is None:
            return jsonify({'error': 'This ID does not exist!'}), 404
        else:
            posts.remove(to_delete)
            return jsonify({'success': 'the post has been deleted'})
    else:
        updated_post = request.get_json()
        new_title = updated_post.get('title')
        new_content = updated_post.get('content')

        to_update = next((post for post in posts if post['id'] == post_id), None)

        if to_update is not None:

            if new_title is not None:
                to_update['title'] = new_title
            if new_content is not None:
                to_update['content'] = new_content

            to_update['id'] = post_id

            return jsonify(to_update), 200
        return jsonify({'error': 'This ID does not exist'})


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    #putting empty string as default return so that I dont have to check for empty title/content AND none
    request_param_title = request.args.get('title', '').strip().lower()
    request_param_content = request.args.get('content', '').strip().lower()
    if request_param_title and request_param_content:
        found_posts = [post for post in posts if request_param_title in post['title'].lower() and request_param_content in post['content'].lower()]
        return jsonify(found_posts)
    if request_param_title:
        found_posts_for_title = [post for post in posts if request_param_title in post['title'].lower()]
        return jsonify(found_posts_for_title)
    if request_param_content:
        found_posts_for_content = [post for post in posts if request_param_content in post['content'].lower()]
        return jsonify(found_posts_for_content)







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
