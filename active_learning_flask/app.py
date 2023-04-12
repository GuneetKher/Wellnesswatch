from flask import Flask, request, jsonify
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle
from urllib.request import urlopen
from flask_cors import CORS
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

app = Flask(__name__)
CORS(app)

# URL of the pickle file in Google Cloud Storage
url_dataframe = 'https://storage.googleapis.com/topic_modelling_bucket/almodel.pkl'

# Load the contents of the URL into a bytes object
with urlopen(url_dataframe) as f:
    datafrmae_pickle_bytes = f.read()

# Load the bytes into a Python object using pickle
al_model = pickle.loads(datafrmae_pickle_bytes)

# URL of the pickle file in Google Cloud Storage
url_token = 'https://storage.googleapis.com/topic_modelling_bucket/altoken.pickle'

# Load the contents of the URL into a bytes object
with urlopen(url_token) as f:
    token_pickle_bytes = f.read()

# Load the bytes into a Python object using pickle
vect = pickle.loads(token_pickle_bytes)

class TextPreprocessor():
    def clean_text(self, text):
        # Remove mentions, hashtags, and URLs
        text = re.sub(r'@[A-Za-z0-9_]+', '', text)
        text = re.sub(r'#', '', text)
        text = re.sub(r'[^\w\s]',' ',text)
        text = re.sub(r'http\S+', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize text and perform POS tagging
        words = nltk.word_tokenize(text)
        pos_tags = nltk.pos_tag(words)
        
        # Remove stopwords and exclude nouns and pronouns
        words = [word for word, tag in pos_tags if word not in stopwords.words('english') and tag not in ['PRP', 'PRP$']]
        
        # Lemmatize words
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        
        # Join words into a cleaned sentence
        cleaned_text = ' '.join(words)
        
        return cleaned_text

@app.route('/predict', methods=['POST'])
def predict():
    text = request.json['text']

    # Preprocess the input text using the TextPreprocessor class
    preprocessed_text = TextPreprocessor().clean_text(text)

    # Vectorize the preprocessed text using the loaded vectorizer
    new_term_matrix = vect.transform([preprocessed_text])

    # Predict the topic label using the LDA model
    class_label = al_model.predict(new_term_matrix)
    print(class_label[0])

    classes = { 0: 'discussion', 1: 'health', 2: 'advice', 3: 'serious', 4: 'positivity', 5: 'work_life', 6: 'none'}

    return jsonify({'class_label': classes[class_label[0]]})

if __name__ == '__main__':
    app.run(debug=True)