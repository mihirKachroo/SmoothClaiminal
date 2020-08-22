# Imports the Google Cloud client library
# provides sentiment analysis and entity recognition/analysis
from google.cloud import language
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import os
from google.oauth2 import service_account

def sample_analyze_entities(text_content):
  client = language_v1.LanguageServiceClient()

  # Available types are PLAN_TEXT and HTML
  type_ = enums.Document.Type.PLAIN_TEXT

  language = "en"
  document = {"content": text_content, "type": type_, "language": language}

  # Available values: NONE, UTF8, UTF16, UTF32
  encoding_type = enums.EncodingType.UTF8
  response = client.analyze_entities(document, encoding_type=encoding_type)

  # Loop through entitites returned from the API
  for entity in response.entities:
      print(u"Representative name for the entity: {}".format(entity.name))

      # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
      print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

      # Get the salience score associated with the entity in the [0, 1.0] range
      # print(u"Salience score: {}".format(entity.salience))

      # Loop over the metadata associated with entity. For many known entities,
      # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
      # Some entity types may have additional metadata, e.g. ADDRESS entities
      # may have metadata for the address street_name, postal_code, et al.
      for metadata_name, metadata_value in entity.metadata.items():
          print(u"{}: {}".format(metadata_name, metadata_value))

      # Loop over the mentions of this entity in the input document.
      # The API currently supports proper noun mentions.
      for mention in entity.mentions:
          print(u"Mention text: {}".format(mention.text.content))


def main():
  import argparse

  example_text = "Lionel Messi has pleaded the board of Barcelona for over two seasons to sign Neymar from Paris Saint-Germain since the former Santos winger left the Camp Nou for a world record fee to France. His departure from Barca was completely unexpected and uncalled for as he performing at an exceptional rate under the guidance of Luis Enrique, however, his sudden exit and the fashion in which he left the club were not taken lightly been many. The skillful winger has not had the best start to life in Paris as he has struggled with injuries all season long and has not had a major impact as expected. Neymar has won three Ligue 1 title medals, however, the Brazilian certainly did not sign just to win the league as the main objective was to win the Champions League. Neymar has stirred a lot of chaos as well, as the Brazilian at one point, was desperate to come back to the Camp Nou to join forces with Lionel Messi and Luis Suarez once again to win the Champions League. However, this season after successfully turning around the tie against Borussia Dortmund in the round of 16 it seems like the Parisian club is the favourites to make it to the final and win their first-ever Champions League trophy. The 28-year-old winger’s contract is set to expire in 2022 with PSG, however, given the club’s recent performance and the guidance by Tuchel, Neymar has reportedly considered signing a new contract with the French club after his current contract expires, according to the Express."
  parser = argparse.ArgumentParser()
  parser.add_argument("--text_content", type=str, default=example_text)
  args = parser.parse_args()

  sample_analyze_entities(args.text_content)

  sample_analyze_entities(example_text)
  
if __name__ == "__main__":
  main()


