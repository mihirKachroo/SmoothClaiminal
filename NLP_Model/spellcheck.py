########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

example_text = "hellooo this iss atest to ssee howgood thes spelll chcker is"

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
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################