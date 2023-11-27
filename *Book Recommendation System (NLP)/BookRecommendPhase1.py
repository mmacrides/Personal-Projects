import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System/goodreads_data.csv")

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

# Replace missing (NaN) values in the 'Description' column with empty strings
df['Description'].fillna('', inplace=True)

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust the number of features as needed

# Fit and transform the book descriptions
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Description'])

# Get the feature names (words) corresponding to the columns in the TF-IDF matrix
feature_names = tfidf_vectorizer.get_feature_names_out()

# Create a DataFrame from the TF-IDF matrix
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

# Concatenate the new DataFrame with the original one
df = pd.concat([df, tfidf_df], axis=1)

# Calculate the cosine similarity based on description data
description_sim_matrix = cosine_similarity(tfidf_df, tfidf_df)
n_description_sim_matrix = 0.5 * (description_sim_matrix + 1)

# Calculate cosine similarity based on genre data
genre_sim_matrix = cosine_similarity(genre_df)
n_genre_sim_matrix = 0.5 * (genre_sim_matrix + 1)

def get_similar_books_with_similarity(book_title, num_recommendations=5, alpha=0.5, beta=0.5):
    book_index = df[df['Book'] == book_title].index[0]
    sim_scores = list(enumerate(n_description_sim_matrix[book_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    similar_books_indices = [i[0] for i in sim_scores[1:num_recommendations + 1]]  # Exclude the book itself
    similar_books = df['Book'].iloc[similar_books_indices]

    # Calculate similarity percentages for description
    description_sim_scores = [i[1] for i in sim_scores[1:num_recommendations + 1]]

    # Calculate similarity percentages for genre
    genre_sim_scores = list(enumerate(n_genre_sim_matrix[book_index]))
    genre_sim_scores = sorted(genre_sim_scores, key=lambda x: x[1], reverse=True)
    genre_sim_scores = [i[1] for i in genre_sim_scores[1:num_recommendations + 1]]

    # Combine the two similarity scores using alpha and beta weights
    combined_similarity_scores = [
        (book, alpha * desc_sim + beta * genre_sim, desc_sim, genre_sim)
        for book, desc_sim, genre_sim in zip(similar_books, description_sim_scores, genre_sim_scores)
    ]

    # Sort the combined similarity scores
    combined_similarity_scores = sorted(combined_similarity_scores, key=lambda x: x[1], reverse=True)

    # Create a DataFrame with the top N books and their similarity scores
    top_books_df = pd.DataFrame(combined_similarity_scores[:num_recommendations], columns=['Book', 'Overall', 'Description', 'Genre'])
    
    return top_books_df


# Example usage:
book_title = "The Help"
similar_books_df = get_similar_books_with_similarity(book_title, num_recommendations=5, alpha=0.8, beta=0.2)
print(similar_books_df.head())