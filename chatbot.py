import requests
def tuling_chatbot(s):
    resp = requests.post("http://www.tuling123.com/openapi/api", data={
        "key": "d59c41e816154441ace453269ea08dba",
        "info": s,
        "userid": "123456"
    })
    resp = resp.json()
    return resp['text']
if __name__ == '__main__':
    pass