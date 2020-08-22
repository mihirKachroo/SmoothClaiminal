########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

# import json to print the data in a neater way
import json

import operator


example_text = "hellooo this iss atest to ssee howgood thes spelll chcker is"

def spell_check(text):
    headers = {
        # Request headers
        # 'Ocp-Apim-Subscription-Key': '{subscription key}',
        'Ocp-Apim-Subscription-Key': '2f7f2504e53041cfacbdc73780ad117f',
    }
    params = urllib.parse.urlencode({
        # Request parameters
        'text': example_text,
        'mode': 'proof',
        'preContextText': '{string}',
        'postContextText': '{string}',
    })

    try:
        # conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn = http.client.HTTPSConnection('hackthe6ix2020resource.cognitiveservices.azure.com')
        conn.request("POST", "/bing/v7.0/spellcheck/?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        # TYPE IS: bytes
        # convert to string
        data = data.decode('utf-8')
        # TYPE IS NOW: str
        # convert to json (dictionary)
        data = json.loads(data)
        # TYPE IS NOW: dict

        # this is to print the data in a neater way if you want:
        # json_object = json.loads(data)
        # json_formatted_str = json.dumps(json_object, indent=2)
        # print(json_formatted_str)

        # Replace incorrect words with correct words
        # text = example_text
        # data = data
        text = text
        data = data
        shifting = 0
        correct = text
        for ft in data['flaggedTokens']:
            offset = ft['offset']
            suggestions = ft['suggestions']
            token = ft['token']

            # find the best suggestion
            suggestions.sort(key=operator.itemgetter('score'), reverse=True)
            substitute = suggestions[0]['suggestion']

            # replace the token by the suggestion
            before = correct[:offset + shifting]
            after = correct[offset + shifting + len(token):]
            correct = before + substitute + after
            shifting += len(substitute) - len(token)
        # print("ORIGINAL:")
        # print(example_text)
        # print("\n")
        # print("CORRECTED:")
        # print(correct)
        return correct
        conn.close()
        
    except Exception as e:
        # print("[Errno {0}] {1}".format(e.errno, e.strerror))
        # print(e)
        return e
