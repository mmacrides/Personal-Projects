from genre import similar_genres
from title import similar_titles
from description import similar_descriptions
import pandas as pd


#book_title = 'The Maze Runner (Maze Runner, #1)'
book_title = 'Legend (Legend, #1)'

booksGenre = similar_genres(book_title)
booksTitle = similar_titles(book_title)
booksDescription = similar_descriptions(book_title)

# Merge booksGenre and booksTitle on the "Book" column
df = pd.merge(booksGenre, booksTitle, on="Book", how="inner")

# Merge the result with booksDescription on the "Book" column
df = pd.merge(df, booksDescription, on="Book", how="inner")

def score(df, genre_weight = 0.25, title_weight = 0.25, description_weight = 0.50):
    df['Score'] = (genre_weight * df['Genre']) + (title_weight * df['Title']) + (description_weight * df['Description'])
    return df

def format(df):
    #Move column 'Score' to be second from the left (index 1)
    col = df.pop('Score')
    df.insert(1, col.name, col)
    # Sort the DataFrame by the "Score" column in descending order
    df = df.sort_values(by='Score', ascending=False)
    return df

def getMetadata(df):
    metadata = pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System/goodreads_data.csv")
    metadata = metadata[['Book', 'Genres', 'Author', 'Avg_Rating', 'Num_Ratings', 'URL']]
    df = pd.merge(df, metadata, on="Book", how="inner")
    return df
#######################################################################################################################################################################################

df = score(df, genre_weight= 0.25, title_weight = 0.25, description_weight = 0.50)
df = format(df)
df = getMetadata(df)
print(df.head())