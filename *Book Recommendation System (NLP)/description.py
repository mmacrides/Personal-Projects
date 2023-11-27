import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System/goodreads_data.csv")
df.head(10)

# Initialize the MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# Replace missing (NaN) values in the 'Description' column with empty strings
df['Description'].fillna('', inplace=True)

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust the number of features as needed

# Fit and transform the book descriptions
tfidf_matrix = tfidf_vectorizer.fit_transform(df['Description'])

# Get the feature names (words) corresponding to the columns in the TF-IDF matrix
feature_names = tfidf_vectorizer.get_feature_names_out()

# Create a DataFrame from the TF-IDF matrix
desc_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

# Concatenate the new DataFrame with the original one
df = pd.concat([df, desc_df], axis=1)

# Calculate the cosine similarity based on description data
description_sim_matrix = cosine_similarity(desc_df)

def getAuthor(book_title):
    selected_author = df.loc[df['Book'] == book_title, 'Author'].values[0]
    return selected_author

def similar_descriptions(book_title):
    if book_title in pd.read_csv("goodreads_data.csv")['Book'].values:
        book_index = df[df['Book'] == book_title].index[0]
        
        # Calculate similarity percentages for description
        desc_sim_scores = list(enumerate(description_sim_matrix[book_index]))
        desc_sim_scores = sorted(desc_sim_scores, key=lambda x: x[1], reverse=True)
        description_sim_scores = [i[1] for i in desc_sim_scores[1:]]

        # Calculate similarity scores
        similar_books_indices = [i[0] for i in desc_sim_scores[1:]]  # Exclude the book itself
        similar_books = df['Book'].iloc[similar_books_indices]
        similarity_scores = [
            (book, genre_sim)
            for book, genre_sim in zip(similar_books, description_sim_scores)
        ]

        # Sort the combined similarity scores
        combined_similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Create a DataFrame with the top N books and their similarity scores
        books = pd.DataFrame(combined_similarity_scores, columns=['Book', 'Description'])
        
        return books
    else:
        books = pd.DataFrame()
        return books