# Personal-Projects
Created a book recommender system that has 10k of the most popular/reviewed books from Goodreads as input. The dataset was already curated and found on Kaggle. Columns include book, author, description, genres, avg_rating, num_ratings, and URL. 

I created three features that attribute to similarity score. I applied tfidfvectorizer() to book and description columns which vectorizes each unique word from both columns. The TF term assigns a non-zero weight if the respective word appears in the title or description. The more often the word occurs, the higher the weight. The IDF term penalizes popular words in the text corpus (opposed to just removing stop words). For example, since "the" will likely occur in the corpus very frequently, I will penalize and lower the weight for this word because it has more "noise" than "signal".

<img width="661" alt="Screenshot 2023-12-03 at 10 21 24 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/120a6440-b115-4ce3-a489-7422f32a6409">

For the genre column, I use a MultiLabelBinarizer() to fit and transform the 'genres' column so that each unique genre is represented as a column and signaled as a 1 or 0 if the respectvie genre is in the list of genres from the original column.

Now that the data is prepared, for title, description, and genre separately, I input a book as parameter and calculate the cosine similarity scores against that respective book.

<img width="659" alt="Screenshot 2023-12-03 at 10 26 44 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/a3f861f0-16b8-432e-a411-a8bc383177cc">
