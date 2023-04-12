# DataSIGNS
CMPT 733 - Term Project

## Wellness Watch

This is the code repository for the term project by the team DataSigns.

### Note

The data used for the tasks has been taken from reddit. It has been pulled from subreddits pertaining to mental health (r/suicidewatch,r/anxiety,r/depression,r/schizophrenia etc) as well as data from subreddits not pertaining to mental health (r/sports, r/technology, r/conspiracy, r/jokes etc) <br>
Overall, our data set contains around 600k datapoints and is not present in this repo due to size limitations. Find data here.

Data is pulled using scripts built to utilise the PushShiftAPI. Learn how it works here.

### Deployed Models 

**Classifier model**: Finetuned transformer model based on Roberta. Deployed here.
Post API call with payload `{"post": [test string here] }`

Note: This is a large sized model, and the API is deployed in serverless manner. So the first call may take longer to respond due to cold start.
These models were also deployed to huggingface.co model repository and can be found here, and here with their tokenizer here. <br>

Check `classifier-testing.ipynb` file's "Testing from remotely loaded models" section to test the model yourself.

**Topic-modelling model**: Trained LDA model. Deployed here.
Post API call with payload `{"text": [test string here] }`

**Categorizer model**: Logistic regression model training through active learning on reddit flairs. Deployed here.
Post API call with payload `{"text": [test string here] }`

You can even use the frontend to check out the Wellness Watch product.

Our test results for the classifier and be found in the repo train_inf.npy and eval_inf.npy files which are numpy array of the format `(correct_label,positivity_probability)` where correct label is 0 for non mental health post and 1 for mental health pertinent post. and the positivity (positive label being pertinent to mental health) probability is a continous number between 0 and 1
