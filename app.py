import streamlit as st

# importing classes
from user import User
from tweet import Tweet
from visualizer import Visualize
from text_cleaner import Text_cleaner

# importing other packages:
import base64
import pandas as pd
import joblib
from PIL import Image
import re

st.title('Tweet Reply Sentiment Extraction')
with st.beta_expander('Application Information'):
    st.markdown('''This is a tweet reply sentiment extractor, and it will assist in retrieving
            the general reaction of a user by determining whether the most recent replies are positive, neutral or negative.
            It is not able to utilize the hashtags, gifs or photos of the replies. It is encouraged
            to use this tool to get an overall picture of the data, and then to explore specific examples (you can explore
            the tweets using the key word tool below!).
            You can help improve its performance when you correct errors in the error correction window.\n
            NOTE: Emojis are transformed into text, in order to assist predictions. 
            If you'd like to check more, check out Emojipedia! (link: https://emojipedia.org/) \n
            Examples:
                😂 -> face_with_tears_of_joy
                🚀 -> rocket
            ''')
current_model = joblib.load('model.pkl')


# SIDEBAR:
st.sidebar.header("Load Tweets")

select_input_method = st.sidebar.selectbox(
    "Select method of loading tweet data:",
    ('CVS file', 'Twitter API'))


# function that pull user api information to access tweets
def twitter_api(N1, N2):
    current_user = User(N1, N2)
    current_user.set_api()
    return current_user.api


# function that takes tweet username, tweet id then scrapes twitter for all of the replies.
def user_input(username, tweet_id, user, tweet_amount):
    current_tweet = Tweet(username, tweet_id, user, tweet_amount)
    current_tweet.reply_scrape()
    return current_tweet.replies_data


# GETTING TWEET DATA:

if select_input_method == 'CVS file':
    try:
        uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=['csv'])
        input_df = pd.read_csv(uploaded_file)

    except:
        st.warning('Upload CVS file')

    with st.sidebar.beta_expander("More Information"):
        st.markdown('''
        The CVS must be split into two columns:\n
        1. the first column should be 'User' and have all user names.\n
        2. the second column should be 'Text' and have all of the tweet text.
        ''')
        cvs_image = None

elif select_input_method == 'Twitter API':
   
    st.sidebar.subheader("API Information:")
    N1 = st.sidebar.text_input('Enter your consumer key:')
    N2 = st.sidebar.text_input('Enter your consumer secret key:')
    try:
        current_user = twitter_api(N1, N2)
    except:
        st.warning('Enter your API information.')
    st.sidebar.subheader("Tweet Information:")
    username = st.sidebar.text_input("Enter the username:")
    tweet_id = st.sidebar.text_input("(Optional) Enter the tweet ID:")
    tweet_amount = st.sidebar.slider("Amount of tweets:", max_value=1000,
                                     value=500, step=5)
    try:
        input_df = user_input(username, tweet_id, current_user, tweet_amount)
    except:
        st.warning('Enter your tweet information. If warning persists, double check API information.')

    with st.sidebar.beta_expander('More Information'):
        st.markdown('''
        API keys are available to those that have access to twitter developer! (link: https://developer.twitter.com/)\n
        The username is the user that you want to get the most recent replies from. You can filter the results 
        for replies to a specific tweet by entering the tweet ID.
        Check the photo below for an example:
        ''')
        tweet_image = Image.open('tweet_info.jpg')
        st.image(tweet_image, caption='Yellow = username, Orange = tweet ID', use_column_width=True)

# MAIN PAGE
try:
# PREDICTION
    # initiate text cleaner so that we can convert emojis to text meanings:
    text_cleaner = Text_cleaner()
    input_df['Text'] = input_df.Text.apply(lambda x: text_cleaner.emoji_to_text(x))
    input_df['Clean'] = input_df.Text.apply(lambda x: text_cleaner.clean_tweet_elements(x))

    # predict and add predictions to new Sentiment column:
    prediction = current_model.classify(input_df.Text)
    input_df['Sentiment'] = prediction

    # reset the indexing incase it changed in prediction process:
    input_df.reset_index(drop=True)

# DATA WINDOW
    st.header('Reply Data')
    st.write('\n')
    placeholder = st.empty()
    placeholder.write(input_df)

    # columns to appear under data window: col1 = error correction, col2 = download csv
    col1, col2 = st.beta_columns(2)

    # Functionality to fix errors:
    with col1:
        st.subheader('Error Correction')
        #Enter number of row with error
        error_number = st.text_input("Input row numbers:")
        with st.beta_expander('How to fix errors'):
            st.markdown('''
            Insert the row number of a tweet, followed by '=' and then the correct sentiment. This will update your 
            visuals and will help the application to do better next time! \n
            Keep all the corrections in the input bar. If you delete one, that tweet will reset to its original sentiment.\n
            TIPS:\n
                1. Try to correct neutral replies, as errors tend to occur here more. After correcting a few, normally the model
                will learn and fix others. (Do this especially if you see a large amount of neutrals in the bargraph below!) \n
                2. Sometimes, it can be difficult to determine whether a reply is positive, negative or neutral. To keep things 
                as consistent as possible, ask yourself 'Does this tweet show a positive or negative opinion about the user or tweet?'
                Neutral replies should be tweets that do not express an opinion about the user or tweet.\n
            Input example:\n
                (1=positive, 4=negative, 20=neutral, 32=negative, 7=neutral, 9=positive) 
            ''')
       
        #This fixes errors:
        if len(error_number) > 0: #checks to see if an error has been inputed
            error_number = error_number.split(',') #splits each error by ','
            possible_sentiments = 'positive, negative, neutral' #possible corrections
            text = []# will be used to partially fit corrections to model
            sentiment = []# will be used to partially fit corrections to model
            #this will loop through each error:
            for i in error_number:
                current_tweet = i.split('=') #split current row number from correction by '='
                if re.search(current_tweet[1], possible_sentiments): #checks to see if correction is in possible corrections
                    input_df['Sentiment'].iloc[int(current_tweet[0])] = current_tweet[1] #changes to correct sentiment
                    text.append(input_df['Text'].iloc[int(current_tweet[0])]) #saves tweet for updating the model
                    sentiment.append(input_df['Sentiment'].iloc[int(current_tweet[0])]) #saves sentiment for updating the model
                    placeholder.write(input_df) #updates the data window

            # this section takes all of the corrections, makes a dataframe, partial fits as new training data
            new_data = {'Text': text, 'Sentiment': sentiment}
            new_train_data = pd.DataFrame(new_data)
            counter = 0
            while counter < 500:
                current_model.partial_fit(new_train_data['Text'], new_train_data['Sentiment'])
                counter = counter + 1
            joblib.dump(current_model, 'model.pkl') # updating pickled model

    # Functionality to download csv (https://discuss.streamlit.io/t/file-download-workaround-added-to-awesome-streamlit-org/1244)
    with col2:
        st.subheader('Download')
        st.write('\n')
        st.write('\n')

        # Streamlit does not have a method for downloading data, this is a workaround that I found:
        csv = input_df.to_csv(index=False, encoding='utf-8')
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}">Download Replies</a>'
        st.markdown(href, unsafe_allow_html=True)
        st.write('\n')
        with st.beta_expander('How to download'):
            st.markdown('''
            Right-click the link above, select save link with a name and save as &lt;some_name&gt;.csv\n
            File name example:\n
                tweetreplies.csv
            ''')

    # VISUAL WINDOW
    st.header('Visualize')
    st.write('\n')

    # user can input custom stopwords to filter out unimportant words
    custom_stop_words = st.text_input('Filter words:')
    with st.beta_expander('More information'):
        st.markdown('''
                    This will filter the words from the word frequency visuals below. Use
                    it to remove frequent words that are related to the context, such as company
                    name, product name or topic. \n
                    Do not add spaces in line. Input example:  \n
                        product,company,stock
                    
                    ''')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    # clean the text to retrieve word frequencies:
    text_cleaner.get_custom_stopwords(custom_stop_words)
    input_df['Clean'] = input_df.Clean.apply(lambda x: text_cleaner.clean(x))

    # activate Visualize class
    visuals = Visualize(input_df)

    # produce visuals
    st.pyplot(visuals.sentiment_ratio())
    st.pyplot(visuals.positive_common_words())
    st.pyplot(visuals.neutral_common_words())
    st.pyplot(visuals.negative_common_words())

    # EXPLORE DATA WITH KEY WORD
    st.header('Explore tweets with a Key word')
    st.write('\n')
    # Data window
    placeholder = st.empty()
    # Key word input
    keyword = st.text_input('Enter a key word:')
    with st.beta_expander('More information'):
        st.markdown('''
        This will match your keyword with every tweet that contains it! \n
        Please enter a single word at a time.
        ''')
    # Finds tweets with keywords and displays new dataframe in data window
    if keyword is not None:
        visuals.get_keyword(keyword)
        keytweets = input_df['Text'].apply(visuals.keyword_search)
        key_df = pd.concat([input_df['User'],keytweets, input_df['Sentiment']], axis=1)
        placeholder.dataframe(key_df.dropna())

except:
    st.warning('Enter your data')
