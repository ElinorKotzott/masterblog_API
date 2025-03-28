from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

posts = [
    {'id': 1, 'title': 'First post', 'content': 'This is the first post.'},
    {'id': 2, 'title': 'Second post', 'content': 'This is the second post.'},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """allows user to add a new post with title and content (post method),
    returns list of posts that can be sorted if user enters sort and direction parameters (get method)"""
    if request.method == 'POST':
        try:
            new_post = request.get_json()
            if new_post is None:
                return jsonify({"error": "Invalid JSON data"}), 400

        except Exception as e:
            return jsonify({"error": f"Error parsing JSON: {str(e)}"}), 400


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
        request_param_sort = request.args.get('sort', '').lower()
        request_param_direction = request.args.get('direction', '').lower()

        if request_param_sort in ['title', 'content'] and request_param_direction in ['asc', 'desc']:
            reverse = (request_param_direction == 'desc')
            return jsonify(sorted(posts, key=lambda post: post[request_param_sort].lower(), reverse=reverse))

        elif request_param_sort or request_param_direction:
            if request_param_sort not in ['title', 'content']:
                return jsonify({'error': 'Invalid sort field. Use "title" or "content".'}), 400

        return jsonify({'error': 'Invalid direction. Use "asc" or "desc".'}), 400
    return jsonify(posts)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def update_or_delete_post(post_id):
    """allows user to delete a post by ID (delete method) or to update an existing
    post with a new title and/or content (put method)"""
    if request.method == 'DELETE':
        to_delete = next((post for post in posts if post['id'] == post_id), None)
        if to_delete is None:
            return jsonify({'error': 'This ID does not exist!'}), 404
        else:
            posts.remove(to_delete)
            return jsonify({'success': 'the post has been deleted'})
    else:
        try:
            updated_post = request.get_json()
            if updated_post is None:
                return jsonify({"error": "Invalid JSON data"}), 400

        except Exception as e:
            return jsonify({"error": f"Error parsing JSON: {str(e)}"}), 400

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
        return jsonify({'error': 'This ID does not exist'}), 404


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """allows user to search posts. both post title and content will be checked"""
    # putting empty string as default return so that I dont have to check for empty title/content AND none
    request_param_title = request.args.get('title', '').strip().lower()
    request_param_content = request.args.get('content', '').strip().lower()

    # starting with all posts and then filtering out the relevant ones
    found_posts = posts

    if request_param_title:
        found_posts = [post for post in found_posts if request_param_title in post['title'].lower()]

    if request_param_content:
        found_posts = [post for post in found_posts if request_param_content in post['content'].lower()]

    if found_posts:
        return jsonify(found_posts)
    # returns empty list if no posts matching the search criteria have been found
    return jsonify([])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
