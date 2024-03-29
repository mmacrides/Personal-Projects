import pandas as pd

path = ("/Users/mattmacrides/Personal-Projects/Book Recommendation System (Content-Filtering)/Data/goodreads_data.csv")

# Scoring function
def score(df, genre_weight=0.2, title_weight=0.1, description_weight=0.7):
    df['Score'] = (genre_weight * df['Genre']) + (title_weight * df['Title']) + (description_weight * df['Description'])
    # Convert the decimal score to percentage with one decimal place
    df['Score'] = (df['Score'] * 100).round(1)
    return df

# Formatting dataframe
def format(df):
    col = df.pop('Score')
    df.insert(1, col.name, col)
    df = df.sort_values(by='Score', ascending=False)
    df = df.drop_duplicates(subset='Book')
    df['Score Number'] = df['Score']
    df['Score'] = df['Score'].astype(str) + '%'
    return df

# Attaching metadata back onto fataframe
def getMetadata(df):
    metadata = pd.read_csv(path)
    metadata = metadata.rename(columns={'Description': 'Descriptions'})
    metadata = metadata[['Book', 'Descriptions', 'Genres', 'Author', 'Avg_Rating', 'Num_Ratings', 'URL']]
    df = pd.merge(df, metadata, on="Book", how="inner")
    return df

def filterPopularity(df, Mainstream = False, Niche = False, Hidden = False):
    # All = All Books
    # Mainstream = Books with 50k+ reviews; Top 30%
    # Niche = Books between 5k - 50k reviews; Top 65% - 30%
    # Hidden = Books with less than 5k reviews; Bottom 35%
    df['Num_Ratings'] = pd.to_numeric(df['Num_Ratings'].str.replace(',', ''), errors='coerce')
    if Mainstream:
        print('mainstream')
        df = df[df['Num_Ratings'] >= 50000]
    elif Niche:
        print('niche')
        df = df[(df['Num_Ratings'] < 50000) & (df['Num_Ratings'] >= 5000)]
    elif Hidden:
        print('hidden')
        df = df[df['Num_Ratings'] < 5000]
    
    df['Num_Ratings'] = df['Num_Ratings'].map('{:,}'.format)
    return df

def getAllBooks():
    df = pd.read_csv(path)
    return df['Book'].tolist()