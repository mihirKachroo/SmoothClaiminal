# Imports the Google Cloud client library
# provides sentiment analysis and entity recognition/analysis
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account



# Function called language_analysis, takes a piece of text as parameter
def language_analysis(text):

  # Instantiates a client
  client = language.LanguageServiceClient.from_service_account_json(r"C:\Users\16479\Downloads\My First Project-d1c715df9f1c.json")

  # Initialize document
  # document = client.document_from_text(text)
  document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)

  #sentiment analysis, gives us sentiment score and also magnitude
  # sentiment score is -1 to +1
  # magnitude is unbounded, 0 to infinity, basically how important is the sentiment overall
  sent_analysis = client.analyze_sentiment(document=document)

  # to show what your options are
  print(dir(sent_analysis))

  # to save time, .sentiment is just one of the methods
  sentiment = sent_analysis.document_sentiment

  # entity analysis, gives us salience
  ent_analysis = client.analyze_entities(document=document)

  entities = ent_analysis.entities

  # return the sentiment and entities
  return sentiment, entities



example_text = "Lionel Messi has pleaded the board of Barcelona for over two seasons to sign Neymar from Paris Saint-Germain since the former Santos winger left the Camp Nou for a world record fee to France. His departure from Barca was completely unexpected and uncalled for as he performing at an exceptional rate under the guidance of Luis Enrique, however, his sudden exit and the fashion in which he left the club were not taken lightly been many. The skillful winger has not had the best start to life in Paris as he has struggled with injuries all season long and has not had a major impact as expected. Neymar has won three Ligue 1 title medals, however, the Brazilian certainly did not sign just to win the league as the main objective was to win the Champions League. Neymar has stirred a lot of chaos as well, as the Brazilian at one point, was desperate to come back to the Camp Nou to join forces with Lionel Messi and Luis Suarez once again to win the Champions League. However, this season after successfully turning around the tie against Borussia Dortmund in the round of 16 it seems like the Parisian club is the favourites to make it to the final and win their first-ever Champions League trophy. The 28-year-old winger’s contract is set to expire in 2022 with PSG, however, given the club’s recent performance and the guidance by Tuchel, Neymar has reportedly considered signing a new contract with the French club after his current contract expires, according to the Express."

# # call language_analysis function, pass in the example text
# sentiment, entities = language_analysis(example_text)

# # print sentiment score (-1 to +1) and magnitude (unbounded)
# print(sentiment.score, sentiment.magnitude)
sentiment, entities= language_analysis(example_text)
print(sentiment.score,sentiment.magnitude)

for e in entities:
  print(e.name, e.type, e.metadata, e.salience)


  

