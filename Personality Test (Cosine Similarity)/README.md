# Personal-Projects
Created a fun similarity test where questions are on a spectrum from 1-10. Each participant fills out their answers in vector format and results are compared using cosine similarity.

Cosine similarity quantifies the cosine of the angle between two vectors, representing their orientation and similarity. The cosine of 0 degrees is 1, meaning the vectors have the same direction (perfect similarity), and the cosine of 90 degrees is 0, indicating they are orthogonal (no similarity).

<img width="650" alt="Screenshot 2023-12-03 at 10 02 20 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/a5e8bc92-325d-4b9e-baad-e9d304af8fbd">

I display a horizontal bar chart to show cosine similarity across all pairs (removed names for confidentiality).

<img width="315" alt="Screenshot 2023-12-03 at 10 03 42 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/6a4c48d6-80ca-40e5-8025-6db5a5899dd0">

I also create dataframes that provide additional analyses:
  1. Dataframe called mostSimilar that displays each person's most similar participant
  2. Dataframe called avgScore that displays each persons average cosine siilarity. A high score
     means the participant shares a lot in common with the group while a low score means the
     participant is most unique.
