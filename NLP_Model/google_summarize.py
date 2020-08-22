# Imports the Google Cloud client library
# provides entity recognition/analysis
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

  # Init entity type arrays
  people = []
  location = []
  address = []
  number = []
  date = []
  other = []

  # Loop through entitites returned from the API
  for entity in response.entities:
      # print(u"Representative name for the entity: {}".format(entity.name))

      # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
      ent = enums.Entity.Type(entity.type).name

      if (ent == "PERSON"):
        people.append(entity.name)

      elif (ent == "LOCATION"):
        location.append(entity.name)

      elif (ent == "ADDRESS"):
        address.append(entity.name)

      elif (ent == "NUMBER"):
        number.append(entity.name)

      elif (ent == "DATE"):
        date.append(entity.name)

      else:
        other.append(entity.name)

      # Get the salience score associated with the entity in the [0, 1.0] range
      # print(u"Salience score: {}".format(entity.salience))

      # Loop over the metadata associated with entity. For many known entities,
      # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
      # Some entity types may have additional metadata, e.g. ADDRESS entities
      # may have metadata for the address street_name, postal_code, et al.
      # for metadata_name, metadata_value in entity.metadata.items():
      #     print(u"{}: {}".format(metadata_name, metadata_value))

      # Loop over the mentions of this entity in the input document.
      # The API currently supports proper noun mentions.
      # for mention in entity.mentions:
      #     print(u"Mention text: {}".format(mention.text.content))

  print("People:")
  print(people)
  print("---------------")

  print("Locations:")
  print(location)
  print("---------------")

  print("Addresses:")
  print(address)
  print("---------------")

  print("Numbers:")
  print(number)
  print("---------------")

  print("Dates:")
  print(date)
  print("---------------")

  print("Other:")
  print(other)

def main():
  import argparse

  example_text = "On October 23, a basement water pipe broke and ended up flooding the area. I wasn't home at the time, so I didn't find out until it was too late. I wanted to get a quote for the repairs."
  parser = argparse.ArgumentParser()
  parser.add_argument("--text_content", type=str, default=example_text)
  args = parser.parse_args()

  sample_analyze_entities(args.text_content)

  # sample_analyze_entities(example_text)
  
if __name__ == "__main__":
  main()


