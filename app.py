from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

# Load pre-saved data at the beginning
popularity_df = pickle.load(open('popularity.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
book_list = pickle.load(open('book_list.pkl', 'rb'))

print("Data loaded successfully.")
print(f"Available books in pt: {pt.index.tolist()[:10]}")  # Debug: Print the first 10 book titles

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popularity_df['Book-Title'].values),
                           author=list(popularity_df['Book-Author'].values),
                           image=list(popularity_df['Image-URL-M'].values),
                           votes=list(popularity_df['num_ratings'].values),
                           rating=np.round(list(popularity_df['avg_ratings'].values), 2)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input').strip()  # Get and strip user input
    print(f"User input: '{user_input}'")  # Print user input for debugging

    # Print all book names in pt index and their indices
    pt_index = list(pt.index)
    print("Books in pt index and their indices:")
    for index, book in enumerate(pt_index):
        print(f"Index: {index}, Book: '{book}'")

    # Check if the user input is in pt.index
    if user_input not in pt_index:
        print("Book not found in the database.")
        return render_template('recommend.html', data=[], message="Book not found in the database.")

    # Find the index of the user input book in pt.index
    indi = pt_index.index(user_input)
    print(f"Index of the book '{user_input}': {indi}")

    # Get similar items based on the index
    similar_items = sorted(list(enumerate(similarity_score[indi])), key=lambda x: x[1], reverse=True)[1:13]
    print(f"Similar items: {similar_items}")

    # Prepare data for rendering
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    print(f"Recommended data: {data}")
    return render_template('recommend.html', data=data)

@app.route('/list')
def listt():
    return render_template('list.html', name=list(books['Book-Title'][1:201].values))

if __name__ == '__main__':
    app.run(debug=True)
