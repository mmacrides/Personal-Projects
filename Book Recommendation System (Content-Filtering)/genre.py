import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System (Content-Filtering)/goodreads_data.csv")
df.head(10)

# Initialize the MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# Parse the string representations into actual lists
gen = [ast.literal_eval(s) for s in df['Genres']]

# Fit and transform the 'genres' column
genre_matrix = mlb.fit_transform(gen)

# Create a DataFrame from the transformed data with custom column names
genre_df = pd.DataFrame(genre_matrix, columns=['is_' + genre for genre in mlb.classes_])

# Concatenate the new DataFrame with the original one
df = pd.concat([df, genre_df], axis=1)

# Calculate the cosine similarity based on genre data
genre_sim_matrix = cosine_similarity(genre_df)


def similar_genres(book_title):
    if book_title in pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System (Content-Filtering)/goodreads_data.csv")['Book'].values:
        book_index = df[df['Book'] == book_title].index[0]
    
        # Calculate similarity percentages for description
        gen_sim_scores = list(enumerate(genre_sim_matrix[book_index]))
        gen_sim_scores = sorted(gen_sim_scores, key=lambda x: x[1], reverse=True)
        genre_sim_scores = [i[1] for i in gen_sim_scores[1:]]

        # Calculate similarity scores
        similar_books_indices = [i[0] for i in gen_sim_scores[1:]]  # Exclude the book itself
        similar_books = df['Book'].iloc[similar_books_indices]
        similarity_scores = [
            (book, genre_sim)
            for book, genre_sim in zip(similar_books, genre_sim_scores)
        ]

        # Sort the combined similarity scores
        combined_similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Create a DataFrame with the top N books and their similarity scores
        books = pd.DataFrame(combined_similarity_scores, columns=['Book', 'Genre'])
        
        return books
    else:
        books = pd.DataFrame()
        return books