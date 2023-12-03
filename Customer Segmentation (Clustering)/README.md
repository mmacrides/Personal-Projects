# Personal-Projects
Overview: Using text clustering method, K-means, to segment mall customers

Three Dimensional:
Initially, I created a 3-dimensional cluster with respect to age, annual income, and spending score. 

<img width="316" alt="Screenshot 2023-12-03 at 8 24 52 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/4013933b-5a79-4489-a55d-c8c9f9dd85d5">

After calclaating the averages per cluster, I was able to generalize clusters:
Cluster 1 (Purple): Annual Income is sub-affluent, generally not willing to spend much, and middle aged
Cluster 2 (Blue): Annual Income is affluent, generally moderately willing to spend money, and young
Cluster 3 (Green): Annual Income is affluent, generally moderately willing to spend money, and older population
Cluster 4 (Yellow): Annual Income is sub-affluent, generally very willing to spend money, and young-middle adult aged

Two Dimensional:
I realized that 3-D clustering might be too convoluted for this use case so I pivoted to traditional 2-D clustering. I decided to segment on annual income and age.

<img width="318" alt="Screenshot 2023-12-03 at 8 26 57 AM" src="https://github.com/mmacrides/Personal-Projects/assets/67166143/c965eff3-9bae-4998-8d0d-8bcf390a613c">

Here are the annotated results:
Cluster 1: Affluent, older generation
Cluster 2: Sub-Affluent, younger generation
Cluster 3: Sub-Affluent, older generation
Cluster 4: Affluent, younger generation

If I were a manager for a store in the mall, I'd like to capture age and income of store shoppers, plug in the model and output the distribution to make sure our marketing strategy is catered towards the majority.
