# DataSIGNS
CMPT 733 - Term Project <br>

<a href="https://youtu.be/oean7fIza20">Presentation</a><br>
<a href="https://medium.com/sfu-cspmp/wellness-watch-enhancing-counselling-outreach-using-machine-learning-c48673878b5a">Blog</a>

## Wellness Watch

This is the code repository for the term project by the team DataSigns.

### Note

The data used for the tasks has been taken from reddit. It has been pulled from subreddits pertaining to mental health (r/suicidewatch,r/anxiety,r/depression,r/schizophrenia etc) as well as data from subreddits not pertaining to mental health (r/sports, r/technology, r/conspiracy, r/jokes etc) <br>
Overall, our data set contains around 600k datapoints and is not present in this repo due to size limitations. Find data <a href="https://drive.google.com/drive/folders/1dmHBVD-hlsQ2uSz2JGKLZKfxaOpMJ8Wr?usp=sharing">here</a> and <a href="https://drive.google.com/drive/folders/12rSc5e6iJ1loQiUgF05qS72hst8zV_l6?usp=sharing">here</a>.

Data is pulled using scripts built to utilise the PushShiftAPI. Learn how it works <a href="https://github.com/GuneetKher/Wellnesswatch/blob/main/Reddit_readme.md">here</a>.

### Deployed Models 

**Classifier model**: Finetuned transformer model based on Roberta. Deployed on GCP. <br>
Post API call with payload `{"post": 'test string here' }` at this endpoint `https://ds-6jwegwyhkq-uc.a.run.app/predict`

Note: This is a large sized model, and the API is deployed in serverless manner. So the first call may take longer to respond due to cold start.
These models were also deployed to huggingface.co model repository and can be found <a href="https://huggingface.co/GuneetK/mh-nmh-lax">here</a>, and <a href='https://huggingface.co/GuneetK/mh-nmh-strict'>here</a> with their tokenizer <a href="https://huggingface.co/GuneetK/mh-nmh-tokenizer">here</a>. <br>

Check `classifier-testing.ipynb` file's "Testing from remotely loaded models" section to test the model yourself.

**Topic-modelling model**: Trained LDA model. Deployed on GCP. <br>
Post API call with payload `{"text": 'test string here' }` at this endpoint `http://34.106.248.124/predict`

**Categorizer model**: Logistic regression model training through active learning on reddit flairs. Deployed on GCP. <br>
Post API call with payload `{"text": 'test string here' }` at this endpoint `http://35.235.75.91/predict`

You can even use the <a href="https://github.com/GuneetKher/Wellnesswatch-ui">frontend</a> to check out the Wellness Watch product.

Our test results for the classifier and be found in the repo <a href="https://github.com/GuneetKher/Wellnesswatch/blob/main/classifier-inference-tests/train_inf.npy">train_inf.npy</a> and <a href="https://github.com/GuneetKher/Wellnesswatch/blob/main/classifier-inference-tests/eval_inf.npy">eval_inf.npy</a> files which are numpy array of the format `(correct_label,positivity_probability)` where correct label is 0 for non mental health post and 1 for mental health pertinent post. and the positivity (positive label being pertinent to mental health) probability is a continous number between 0 and 1. The accuracy of the classifier model during our testing was 97%.
