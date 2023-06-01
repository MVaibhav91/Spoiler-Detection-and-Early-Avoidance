from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

def is_spoiler(review):

    classifier = load_model("trained_models/imdb_model_2epochs.h5")
    maxlen = 10000
    num_words = 20000
    word_index = imdb.get_word_index()

    review = review.lower().split()

    review = [word_index[word] + 2 if word in word_index else 1 for word in review]

    review = [word for word in review if word < num_words]

    review = pad_sequences([review], maxlen=maxlen)
    prediction = classifier.predict(review)[0][0]
    print("Prediction: ",prediction)
    if prediction >= 0.8:
        return True
    else:
        return False
