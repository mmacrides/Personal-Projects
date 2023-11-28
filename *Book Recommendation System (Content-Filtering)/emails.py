from flask_mail import Mail, Message
import pandas as pd

def configure_mail(app):
    mail = Mail(app)
    return mail

def send_email(email, book_title, book_data):
    mail = Mail()  # Create a new instance of Mail
    msg = Message('Top 10 Similar Books', sender= "mattmacrides@gmail.com", recipients=[email])
    book_data = pd.DataFrame(book_data)
    book_data['Num_Ratings'] = book_data['Num_Ratings'].apply(lambda x: f"{x:,}")
    book_data['Score'] = book_data['Score'].apply(lambda x: f"{x:.1f}%")
    email_body = f"Hi {email},\n\nHere are the top 10 similar books based on {book_title}:\n\n"
    for index, (row_index, book) in enumerate(book_data.iterrows(), start=1):
        email_body += f"{book['Book']}\n"
        email_body += f"         Similarity Score: {book['Score']}\n"
        email_body += f"         Rating: {book['Avg_Rating']}  |  # of Reviews: {book['Num_Ratings']}\n"
        email_body += f"         URL: {book['URL']}\n\n"
    msg.body = email_body
    mail.send(msg)
