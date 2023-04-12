import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from multiprocessing import Pool
import pandas as pd

# Load the documents to be modeled
df = pd.read_csv('consolidatedmhlong_cleaned.csv')
print(df.columns)
documents = np.array(df['clean_texts'].dropna())#[:1000]

# Preprocess the data
vectorizer = CountVectorizer(stop_words='english', token_pattern=r'\b\w+\b')
X = vectorizer.fit_transform(documents)

# Define the number of topics
num_topics = 15

# Define the number of CPU cores to use
#num_cores = 4

# Define the LDA model
lda = LatentDirichletAllocation(n_components=num_topics, n_jobs=-1)

# Train the LDA model
lda.fit(X)

import pickle
with open('lda_model.pickle', 'wb') as f:
    pickle.dump(lda, f)

# Print the topics and their top keywords
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i]
                    for i in topic.argsort()[:-5 - 1:-1]]))
