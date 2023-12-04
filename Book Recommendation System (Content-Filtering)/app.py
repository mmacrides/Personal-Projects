from flask import Flask, render_template, request, jsonify
from genre import similar_genres
from title import similar_titles
from description import similar_descriptions, getAuthor
from processing import getMetadata, score, format, getAllBooks, filterPopularity
from emails import configure_mail, send_email
import pandas as pd

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'mattmacrides@gmail.com'
app.config['MAIL_PASSWORD'] = 'grxy slvy wrjo chbm'
app.config['MAIL_DEFAULT_SENDER'] = 'mattmacrides@gmail.com'

# Configure mail with the app
mail = configure_mail(app)

def score(df, genre_weight, title_weight, description_weight):
    df['Score'] = (genre_weight * df['Genre']) + (title_weight * df['Title']) + (description_weight * df['Description'])
    df['Score'] = (df['Score'] * 100).round(1)
    return df

def get10Books(book_title, genre_weight, title_weight, description_weight, excludeAuthor=False, mainstream = False, niche = False, hidden = False):
    # Retrieve similarity data
    booksGenre = similar_genres(book_title)
    booksTitle = similar_titles(book_title)
    booksDescription = similar_descriptions(book_title)
    if booksTitle.empty:
        return pd.DataFrame()
    else:
        # Merge similarity data and add metadata columns back into dataset
        df = pd.merge(booksGenre, booksTitle, on="Book", how="inner")
        df = pd.merge(df, booksDescription, on="Book", how="inner")
        df = getMetadata(df)
        # Filter out books from the same author
        if excludeAuthor:
            selectedAuthor = getAuthor(book_title)
            df = df[df['Author'] != selectedAuthor]
        # Filter popularity functionality
        df = filterPopularity(df, mainstream, niche, hidden)
        print(mainstream)
        # Score and format data set
        df = score(df, genre_weight, title_weight, description_weight)
        df = format(df)
        selected_columns = ['Book', 'Score', 'Score Number', 'Descriptions', 'Genres', 'Author', 'Avg_Rating', 'Num_Ratings', 'URL']
        df = df[selected_columns]
        df = df.drop_duplicates(subset=['Book', 'Author'])
        df = df.head(10)
        # Convert DataFrame to list of dictionaries
        return df.to_dict(orient='records')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get weights from UI
        book_title = request.form['book_title']
        genre_weight = float(request.form.get('genre_weight'))
        title_weight = float(request.form.get('title_weight'))
        description_weight = float(request.form.get('description_weight'))
        # Get the status of the 'exclude_author' checkbox
        excludeAuthor = 'exclude_author' in request.form
        mainstream = 'book_visibilityMainstream' in request.form
        #mainstream = request.form.get('book_visibilityMainstream')
        niche = request.form.get('book_visibilityNiche')
        hidden = request.form.get('book_visibilityHidden')
        print('Form Data:', request.form)

        top_10_similar_books = get10Books(book_title, genre_weight, title_weight, description_weight, excludeAuthor, mainstream, niche, hidden)
        script = f"<script>var book_title = '{book_title}';</script>"
        return render_template('result.html', table=top_10_similar_books, email_data=top_10_similar_books, script=script)

    return render_template('index.html', all_books=getAllBooks())

@app.route('/send_email', methods=['POST'])
def send_email_route():
    try:
        data = request.get_json()
        print('Received data:', data)
        
        email = data.get('email')
        top_10_similar_books = data.get('book_data', [])
        book_title = data.get('book_title', '')
        
        print('Email:', email)
        print('Top 10 Similar Books:', top_10_similar_books)
        print('Book Title:', book_title)
        
        send_email(email, book_title, top_10_similar_books)
        return jsonify({'message': 'Email sent successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
