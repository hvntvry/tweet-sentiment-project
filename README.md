# tweet-sentiment-project
This is an application that can scrap twitter replies and predict a sentiment. It also provides various graph visuals. 

  ## Installation: 
You can use the application by going to https://tweet-sentiment-application.herokuapp.com/. If you'd like to use it locally then download the following files:
  app.py
  model.pkl
  prediction.py
  text_cleaner.py
  tweet.py
  user.py
  visualizer.py
  Optional: amazon_test_data.csv
  
  Using a terminal type:
  ```terminal
   streamlit run app.py
   ```
   
   ## File descriptions:
    Data = contains the main data used to train the model 
    
    Processed = contains the output data of the data_processing.py script
    
    Procfile = used by heroku to run the application
    
    amazon_test_data.csv = around 1000 tweets scraped from the amazon twitter account. Use this to test the application if you don't have API credentials
    
    app.py = the main streamlit app
    
    data_processing.py = the script used to clean and prepare the data to train the model
    
    model.pkl = the trained model
    
    model.py = the script used to train and test the model
    
    prediction.py = used in model.py, a class that contains the different sklearn models and their settings
    
    requirements.txt = the required packages
    
    text_cleaner.py = the class used in app.py to clean tweets
    
    tweet.py = the class used in app.py to access twitter API and retrieve replies
    
    tweet_info.jpg = a visual to show how to find tweet information
    
    user.py = the class used in app.py to authorize twitter API access 
    
    visualizer.py = the class used in app.py to provide data visuals, bar graphs and key word searching.
    
    
    
    
  
