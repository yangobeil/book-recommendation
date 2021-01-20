import pickle

from flask import Flask, request, render_template, jsonify
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

app = Flask(__name__)

# load data and extract all the vectors
with open('books_long_embeddings_single.pkl', 'rb') as f:
    book_data = pickle.load(f)
vectors = [item['vector'] for item in book_data]
isbn_list = [item['ISBN'] for item in book_data]
X = np.array(vectors)

# calculate similarity based on Euclidean distance
print('Calculating euclidean distances')
sim = euclidean_distances(X)
indices = np.vstack([np.argsort(-arr) for arr in sim])

# calculate similarity based on cosine distance
print("Calculating cosine distances")
cos_sim = cosine_similarity(X)
cos_indices = np.vstack([np.argsort(-arr) for arr in cos_sim])

# find most similar books for each case
print("Finding similar books")
for i, book in enumerate(book_data):
    book['euclidean'] = indices[i][1:21]
    book['cosine'] = cos_indices[i][1:21]


@app.route("/", methods=['GET', 'POST'])
def template_test():
    if request.method == 'POST':
        selected_title = request.form.get('selected_title')
        selected_book = next(item for item in book_data if item['title'] == selected_title)
        similar_books = [book_data[i] for i in selected_book['cosine']]
        return render_template('index.html',
                               list_books=book_data,
                               book_selected=selected_book,
                               similar_books=similar_books[:6])
    return render_template('index.html', list_books=book_data)


@app.route("/recommendations", methods=['GET'])
def get_recommendations():
    isbn = request.args.get('isbn', default=None, type=str)
    num_reco = request.args.get("number", default=5, type=int)
    distance = request.args.get("distance", default="cosine", type=str)
    field = request.args.get("field", default="ISBN", type=str)
    if not isbn:
        return jsonify("Missing ISBN for the book"), 400
    elif distance not in ["cosine", "euclidean"]:
        return jsonify("Distance can only be cosine or euclidean"), 400
    elif num_reco not in range(1, 21):
        return jsonify("Can only request between 1 and 20 books"), 400
    elif isbn not in isbn_list:
        return jsonify("ISBN not in supported books"), 400
    elif field not in book_data[0].keys():
        return jsonify("Field not available in the data"), 400
    else:
        try:
            selected_book = next(item for item in book_data if item['ISBN'] == isbn)
            similar_books = [book_data[i][field] for i in selected_book[distance]]
            return jsonify(similar_books[:num_reco]), 200
        except Exception as e:
            return jsonify(str(e)), 500


if __name__ == '__main__':
    app.run()