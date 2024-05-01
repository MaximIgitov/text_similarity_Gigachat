import requests
import numpy as np
import base64
import uuid
import json
from gigachat import GigaChat
from sklearn.metrics.pairwise import cosine_similarity
#from base_worker import Worker


class RecSystemWorker():
    def __init__(self):
        super(RecSystemWorker, self).__init__()
        ...


    def token(self):
        token_url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
        client_id = '0f02ee18-f159-45b6-a20e-963bf257bdcd'
        client_secret = 'd75e0f68-7220-46d7-80bb-1f2f34d56b5b'
        request_id = str(uuid.uuid4())
        token_data = {
            'scope': 'GIGACHAT_API_PERS'
        }
        credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        token_headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': request_id
        }
        response = requests.post(token_url, headers=token_headers, data=token_data, verify=False)
        return response.json()['access_token']


    def embedding_from_llm(self, s : str) -> list:
        url = "https://gigachat.devices.sberbank.ru/api/v1/embeddings"

        payload = json.dumps({
          "model": "Embeddings",
          "input": s
        })
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': f'Bearer {self.token()}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        # status_code == 200 - код успешного запроса
        if response.status_code == 200:
            response_json = response.json()
            embedding = response_json['data'][0]['embedding']
            return embedding
        else:
            return 0


    def cos_sim(self, text_1: str, text_2: str) -> float:
        embedding_1 = np.array(self.embedding_from_llm(text_1)).reshape(1, -1)
        embedding_2 = np.array(self.embedding_from_llm(text_2)).reshape(1, -1)
        similarity = cosine_similarity(embedding_1, embedding_2)
        return float(similarity[0][0])
    

    def _process(self):
        ...
        pass

text_similarity_model = RecSystemWorker()
s = 'белый'
s1 = 'белый'
similarity = text_similarity_model.cos_sim(s, s1)
print(similarity)