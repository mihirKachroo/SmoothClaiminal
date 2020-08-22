# Imports the Google Cloud client library
# provides entity recognition/analysis
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud.language import types
import os
from google.oauth2 import service_account

# Function for entity analysis
def sample_analyze_entities(text_content):
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

      # Get the salience score associated with the entity in the [0, 1.0] range
      # print(u"Salience score: {}".format(entity.salience))

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

  if (len(people) != 0):
    print("People:")
    print(set(people))
    print("---------------")

  if (categories):
    print("Possible insurance policies:")
    print(set(categories))
    print("---------------")

  if (len(price) != 0):
    print("Prices:")
    print(price)
    print("---------------")

  if (len(date) != 0):
    print("Dates:")
    print(set(date))
    print("---------------")

  if (len(location) != 0):
    print("Locations:")
    print(set(location))
    print("---------------")

  if (len(address) != 0):
    print("Addresses:")
    print(set(address))
    print("---------------")

  if (len(orgs) != 0):
    print("Organizations:")
    print(set(orgs))
    print("---------------")

  if (len(number) != 0):
    print("Numbers:")
    print(set(number))
    print("---------------")

  if (len(other) != 0):
    print("Other:")
    print(set(other))


# Function for sentiment analysis
def language_analysis(text):

  # Instantiates a client
  client = language_v1.LanguageServiceClient.from_service_account_json("./cred.json")

  # Initialize document
  # document = client.document_from_text(text)
  document = types.Document(content=text,type=enums.Document.Type.PLAIN_TEXT)

  #sentiment analysis, gives us sentiment score and also magnitude
  # sentiment score is -1 to +1
  # magnitude is unbounded, 0 to infinity, basically how important is the sentiment overall
  sent_analysis = client.analyze_sentiment(document=document)

  # to show what your options are
  # print(dir(sent_analysis))

  # to save time, .sentiment is just one of the methods
  sentiment = sent_analysis.document_sentiment

  # entity analysis, gives us salience
  ent_analysis = client.analyze_entities(document=document)

  entities = ent_analysis.entities

  # return the sentiment and entities
  return sentiment, entities


# Import libraries for text summarization
from gensim.summarization import summarize
from gensim.summarization import keywords

def main():
  import argparse

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

  parser = argparse.ArgumentParser()
  parser.add_argument("--text_content", type=str, default=example_text)
  args = parser.parse_args()


  print("FULL TEXT: \n" + args.text_content + "\n")

  print("SUMMARY:")
  print(summarize(args.text_content, word_count=90) + "\n")

  print("ENTITY ANALYSIS:")
  sample_analyze_entities(args.text_content)
  print("\n")

  # call language_analysis function, pass in text
  sentiment, entities = language_analysis(args.text_content)
  
  # prints sentiment score (-1 to +1) and magnitude (unbounded)
  print("SENTIMENT SCORE:")
  print(sentiment.score) 
  
if __name__ == "__main__":
  main()


