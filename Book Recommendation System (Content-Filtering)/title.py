import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

path = ("/Users/mattmacrides/Personal-Projects/Book Recommendation System (Content-Filtering)/Data/goodreads_data.csv")
df = pd.read_csv(path)
df.head(10)

# Initialize the MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# Replace missing (NaN) values in the 'Book' column with empty strings
df['Book'].fillna('', inplace=True)

# Initialize the TF-IDF vectorizer
book_tfidf_vectorizer = TfidfVectorizer()  # You can adjust the number of features as needed

# Fit and transform the book descriptions
book_tfidf_matrix = book_tfidf_vectorizer.fit_transform(df['Book'])

# Get the feature names (words) corresponding to the columns in the TF-IDF matrix
feature_names = book_tfidf_vectorizer.get_feature_names_out()

# Create a DataFrame from the TF-IDF matrix
book_df = pd.DataFrame(book_tfidf_matrix.toarray(), columns=feature_names)

# DECIDED NOT TO REMOVE STOP WORDS: https://opensourceconnections.com/blog/2023/01/24/10-reasons-why-you-shouldnt-remove-stop-words/
#Iterate over columns and remove columns consisting of stop words
#nltk.download('stopwords')
#stop_words = set(word.lower() for word in stopwords.words('english'))

# Create a list to store columns to drop
#columns_to_drop = []

# Iterate over columns and identify columns to drop
#for col in book_df.columns:
    #if all(word.lower() in stop_words for word in col.split()):
        #columns_to_drop.append(col)
        #print(f"Dropping column: {col}")

# Drop identified columns
#book_df.drop(columns=columns_to_drop, inplace=True)

# Concatenate the new DataFrame with the original one
df = pd.concat([df, book_df], axis=1)

# Calculate the cosine similarity based on book data
book_sim_matrix = cosine_similarity(book_df)

def similar_titles(book_title):
    if book_title in pd.read_csv(path)['Book'].values:
        book_index = df[df['Book'] == book_title].index[0]
        
        # Calculate similarity percentages for description
        bk_sim_scores = list(enumerate(book_sim_matrix[book_index]))
        bk_sim_scores = sorted(bk_sim_scores, key=lambda x: x[1], reverse=True)
        book_sim_scores = [i[1] for i in bk_sim_scores[1:]]

        # Calculate similarity scores
        similar_books_indices = [i[0] for i in bk_sim_scores[1:]]  # Exclude the book itself
        similar_books = df['Book'].iloc[similar_books_indices]
        similarity_scores = [
            (book, genre_sim)
            for book, genre_sim in zip(similar_books, book_sim_scores)
        ]

        # Sort the combined similarity scores
        combined_similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Create a DataFrame with the top N books and their similarity scores
        books = pd.DataFrame(combined_similarity_scores, columns=['Book', 'Title'])
        
        return books
    else:
        books = pd.DataFrame()
        return books