import re
import string
import spacy
from nltk.corpus import stopwords
from emot.emo_unicode import UNICODE_EMO

stopwords = stopwords.words('english')
nlp = spacy.load('en_core_web_sm')
punctuations = string.punctuation

'''
This class is used to clean texts aka remove stopwords, punctuation, emojis, hashtags, urls and mentions. It is used 
primarily to clean the tweets before extracting word frequencies for visualizations. It is also used before prediction 
of tweets to convert emojis to text. It is not used for training the model because the sklearn package includes 
vectorization, which automatically tokenizes and removes stopwords.
'''

class Text_cleaner:
    def __init__(self):
        self.stopwords = stopwords
        self.punctuations = punctuations

    def get_custom_stopwords(self, custom_stopwords):
        self.custom_stopwords = custom_stopwords.split(',')
        self.stopwords.extend(self.custom_stopwords)

    def clean(self, text):
        hashtags = re.compile(r"^#\S+|\s#\S+")
        mentions = re.compile(r"^@\S+|\s@\S+")
        urls = re.compile(r"https?://\S+")
        text = re.sub(urls, '', text)
        text = hashtags.sub('', text)
        text = mentions.sub('', text)
        text = nlp(text, disable=['parser', 'ner'])  # why stop parser/ner?
        tokens = [tok.lemma_.lower().strip() for tok in text if
                  tok.lemma_ != '-PRON-']  # what is strip() doing
        tokens = [tok for tok in tokens if tok not in self.stopwords
                  and tok not in self.punctuations]
        cleaned_text = ' '.join(tokens)
        return cleaned_text

    # thanks to "https://medium.com/towards-artificial-intelligence/emoticon-and-emoji-in-text-mining-7392c49f596a"
    def emoji_to_text(self, text):
        for emot in UNICODE_EMO:
            text = text.replace(emot,
                                "_".join(UNICODE_EMO[emot].replace(",", "").replace(":", "").split()))
        return text
