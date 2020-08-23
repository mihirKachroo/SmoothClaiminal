# Imports the Google Cloud client library
# provides entity recognition/analysis
import google
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account

# Function for entity analysis
def analyze_entities(text_content):
  client = language_v1.LanguageServiceClient.from_service_account_json("./cred.json")

  # Available types are PLAN_TEXT and HTML
  type_ = enums.Document.Type.PLAIN_TEXT

  language = "en"
  document = {"content": text_content, "type": type_, "language": language}

  # Available values: NONE, UTF8, UTF16, UTF32
  encoding_type = enums.EncodingType.UTF8
  response = client.analyze_entities(document, encoding_type=encoding_type)

  # Init entity type arrays
  people = []
  location = []
  address = []
  number = []
  date = []
  price = []
  orgs = []
  other = []

  # Loop through entitites returned from the API
  for entity in response.entities:
      # print(u"Representative name for the entity: {}".format(entity.name))

      # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
      ent = enums.Entity.Type(entity.type).name
      ent_len = len((entity.name).split(" "))


      if (ent == "PERSON" and (ent_len == 2 or ent_len == 3)):
        people.append(entity.name)

      elif (ent == "LOCATION"):
        for mention in entity.mentions:
          if enums.EntityMention.Type(mention.type).name != 'PROPER':
            location.append(entity.name.lower())
          
          else:
            location.append(entity.name)

      elif (ent == "ADDRESS"):
        address.append(entity.name)

      elif (ent == "NUMBER"):
        number.append(entity.name)

      elif (ent == "DATE"):
        date.append(entity.name)

      elif (ent == "PRICE"):
        price.append(entity.name)

      elif (ent == "ORGANIZATION"):
        orgs.append(entity.name)

      else:
        other.append(entity.name.lower())

  # Filter price if more than 1 exists
  if (len(price) > 0):
    price[0].replace('$','').replace(',','')

  if (len(price) > 1):
    min = float(price[0].replace('$','').replace(',',''))
    max = 0

    for p in price:
      num = float(p.replace('$','').replace(',',''))
      if (num < min):
        min = num

      if (num > max):
        max = num
    
    price = [min, max]

  # Process the information to determine type of claim (Home, Auto, Health, Dental?)
  possible_auto = ['car', 'truck', 'bus', 'van', 'minivan', 'stolen']
  possible_health = ['hospital', 'emergency room', 'emergency', 'bone', 'cut', 'blood', 'bleeding', 'bleed', 'scar', 'surgery']
  possible_dental = ['dentist', 'dental', 'dental office', 'teeth', 'gums', 'crown', 'molar', 'cavity']
  possible_home = ['home', 'house', 'basement', 'room', 'living room', 'sofa', 'couch', 'tv', 'computer', 'stolen']

  categories = []

  for auto in possible_auto:
    if auto in other:
      categories.append("Auto")

  for health in possible_health:
    if health in location or health in other:
      categories.append("Health")

  for dental in possible_dental:
    if dental in location or dental in other:
      categories.append("Dental")

  for home in possible_home:
    if home in location or home in other:
      categories.append("Home")

  # Remove duplicates
  categories = set(categories) if categories else {}
  price = set(price) if price else {}
  date = set(date) if date else {}
  location = set(location) if location else {}
  address = set(address) if address else {}

  return [categories, price, date, location, address]

# Function for sentiment analysis
def language_analysis(text):

  # Instantiates a client
  client = language_v1.LanguageServiceClient.from_service_account_json("./cred.json")

  # Initialize document
  # document = client.document_from_text(text)
  document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)

  #sentiment analysis, gives us sentiment score and also magnitude
  # sentiment score is -1 to +1
  sent_analysis = client.analyze_sentiment(document=document)

  # to save time, .sentiment is just one of the methods
  sentiment = sent_analysis.document_sentiment

  # return the sentiment
  return sentiment


# Import libraries for text summarization
from gensim.summarization import summarize
from gensim.summarization import keywords


# Get summary of text
def get_summary(text):
  return summarize(text, word_count=90)


# Get the urgency (0 being least, 1 being most)
def getUrgency(text):
  # call language_analysis function, pass in text
  sentiment = language_analysis(text)
  
  return 0.5 + (sentiment.score/2)

def main():
  example_text = "August 21, 2020 Mr. Abner Kenny Northern Insurance P.O. Box 337 Milwaukee, WI Date of incident: July 12, 2020 \
Dear Mr. Kenny As you know, I was involved in a collision with a van owned by your insured on Chestnut St. in Waukesha, WI. I was \
waiting at a stop sign, when the Jenkins Hardware van rear-ended me. I was not injured, but my car suffered a fair amount of damage, \
which, despite repeated phone calls, Northern Insurance has so far refused to pay for. The Jenkins driver was obviously negligent. \
He rear-ended someone waiting at a stop sign. It is an open-and-shut case. As a result of this incident, my trunk was caved in. \
I have a small Honda, and small cars don’t tend to fare very well when they are hit by commercial vans. I brought it to my usual \
mechanic, who recommended that I go to Waukesha Body Shop, where they gave me an estimate for $4,600 for a full repair. I have attached \
another copy of the estimate, although I have sent it to you twice before. You also have pictures of the damage. My car is only 2 years \
old, and is worth far more than that. I understand that your estimator valued the repair costs at $4,000. That is not that far off. I \
don’t understand why we haven’t been able to agree on a repair price. Taking into account your insured’s absolute liability and my damages \
in this case, I demand $4,600.00 to settle this case. This is not a complex claim. If I do not hear from you in one week, I will call the \
Wisconsin Department of Insurance to file a complaint against you. Very truly yours, Fred Smith."
  print(analyze_entities(example_text))

if __name__ == '__main__':
  main()