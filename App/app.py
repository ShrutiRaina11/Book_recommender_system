from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pvt = pickle.load(open('pvt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
books_name = list(books.drop_duplicates('Book-Title')['Book-Title'].values)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_ratings'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    print("helo")
    return render_template('recommend.html', books_name=books_name)


@app.route('/recommend_books', methods=['GET'])
def recommend_books():
    user_input = request.args.get('user_input')

    if user_input not in books['Book-Title'].values:
        return render_template('recommend.html', books_name=books_name, message="No book found", user_input=user_input)

    book_index = np.where(pvt.index == user_input)[0][0]
    distances = similarity_scores[book_index]
    books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    suggestions = []
    for book_index in books_list:
        item = []
        temp_df = books[books['Book-Title'] == pvt.index[book_index[0]]].drop_duplicates('Book-Title')
        item.extend(list(temp_df['Book-Title'].values))
        item.extend(list(temp_df['Book-Author'].values))
        item.extend(list(temp_df['Image-URL-M'].values))

        suggestions.append(item)

    return render_template('recommend.html', books_name=books_name, data=suggestions, user_input=user_input)


if __name__ == '__main__':
    app.run(debug=True)
