# Personal-Projects
Created a book recommender system that has 10k of the most popular/reviewed books from Goodreads as input. The dataset was already curated and found on Kaggle. Columns include book, author, description, genres, avg_rating, num_ratings, and URL. 

I created three features that attribute to similarity score. I applied tfidfvectorizer() to book and description columns which vectorizes each unique word from both columns. The TF term assigns a non-zero weight if the respective word appears in the title or description. The more often the word occurs, the higher the weight. The IDF term penalizes popular words in the text corpus (opposed to just removing stop words). For example, since "the" will likely occur in the corpus very frequently, I will penalize and lower the weight for this word because it has more "noise" than "signal".

<img width="661" alt="Screenshot 2023-12-03 at 10 21 24 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/120a6440-b115-4ce3-a489-7422f32a6409">

For the genre column, I use a MultiLabelBinarizer() to fit and transform the 'genres' column so that each unique genre is represented as a column and signaled as a 1 or 0 if the respectvie genre is in the list of genres from the original column.

Now that the data is prepared, for title, description, and genre separately, I input a book as parameter and calculate the cosine similarity scores against that respective book. In my front-end UI, you will see that there are beta weights for each feature. This is for the user to play around with to see if they want to weight similarity more based on description, title, or genre. I believe 0.7 for description, 0.2 for genre, and 0.1 for title is a good balance.

<img width="659" alt="Screenshot 2023-12-03 at 10 26 44 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/a3f861f0-16b8-432e-a411-a8bc383177cc">

Then I create a web application using Flask, HTML, and CSS to dynamically search for books and find their top 10 most similar books. The Flask file is app.py and the web files are under the template folder. I also added a filter called "exclude same author" in case you didn't want to retrieve results from the same author you are searching with. I also added a filter relating to the number of reviews a book has (popularity/visibility). Here is how I segmented the categories:
    # All = All Books
    # Mainstream = Books with 50k+ reviews; Top 30%
    # Niche = Books between 5k - 50k reviews; Top 65% - 30%
    # Hidden = Books with less than 5k reviews; Bottom 35%

Because this website is hosted locally, my friends aren't able to access this application. However, I added an email functionality that I can sent the top 10 results of a particular book.

Below are my front-end screenshots:

Landing/Main Page:
<img width="765" alt="Screenshot 2023-12-03 at 10 35 56 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/461d7c55-1f8a-4069-8cfb-9129b8314550">

Showing Top 10 Results for The Maze Runner:
<img width="1015" alt="Screenshot 2023-12-03 at 10 38 15 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/9b964e1f-630e-40e5-911f-5b04567e9d7c">

Using the Details dropdown:
<img width="959" alt="Screenshot 2023-12-03 at 10 38 40 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/c95a130f-633c-4ef3-9cb9-54503ceeeb41">

Email Sent with Results:
<img width="483" alt="Screenshot 2023-12-03 at 10 39 28 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/353c7d12-31f8-43b2-adc0-07826ac0f2ae">
