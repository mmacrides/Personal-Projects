import pandas as pd

def score(df, genre_weight=0.2, title_weight=0.1, description_weight=0.7):
    df['Score'] = (genre_weight * df['Genre']) + (title_weight * df['Title']) + (description_weight * df['Description'])
    # Convert the decimal score to percentage with one decimal place
    df['Score'] = (df['Score'] * 100).round(1)
    return df

def format(df):
    col = df.pop('Score')
    df.insert(1, col.name, col)
    df = df.sort_values(by='Score', ascending=False)
    df = df.drop_duplicates(subset='Book')
    df['Score Number'] = df['Score']
    df['Score'] = df['Score'].astype(str) + '%'
    return df

def getMetadata(df):
    metadata = pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System (Content-Filtering)/goodreads_data.csv")
    metadata = metadata.rename(columns={'Description': 'Descriptions'})
    metadata = metadata[['Book', 'Descriptions', 'Genres', 'Author', 'Avg_Rating', 'Num_Ratings', 'URL']]
    df = pd.merge(df, metadata, on="Book", how="inner")
    return df

def filterPopularity(df, Mainstream = False, Niche = False, Hidden = False):
    # All = All Books
    # Mainstream = Books with 50k+ reviews; Top 30%
    # Niche = Books between 5k - 50k reviews; Top 65% - 30%
    # Hidden = Books with less than 5k reviews; Bottom 35%
    if (Mainstream):
        df = df[df['Num_Ratings'] >= 50000]
    if (Niche):
        df = df[df['Num_Ratings'] < 50000]
        df = df[df['Num_Ratings'] >= 5000]
    if(Hidden):
        df = df[df['Num_Ratings'] < 5000]
    return df

def getAllBooks():
    df = pd.read_csv("/Users/mattmacrides/Personal-Projects/Book Recommendation System (Content-Filtering)/goodreads_data.csv")
    return df['Book'].tolist()