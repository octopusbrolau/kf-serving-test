from __future__ import print_function

import io
import os
import time
import base64
import json
import time

import requests
import pickle
import onepanel.core.api
from onepanel.core.api.rest import ApiException
import onepanel.core.auth
from pprint import pprint


# ## Get Onepanel Access Token for network requests

# In[2]:

# username = 'admin'
# token = '5aed14f5bffc9f86fd0fb2745519f2ff'
# host = 'http://onepanel.niuhongxing.cn/api'
# access_token = onepanel.core.auth.get_access_token(username=username, token=token, host=host)
access_token = onepanel.core.auth.get_access_token()
print('---access_token----', access_token)
# Configure API key authorization: Bearer
configuration = onepanel.core.api.Configuration(
    host=host,
    api_key={
        'authorization': access_token
    }
)
configuration.api_key_prefix['authorization'] = 'Bearer'


# In[5]:


namespace = 'mp'
model_name = 'faster-rcnn-torchserve'


# In[6]:


# Get status, endpoint
with onepanel.core.api.ApiClient(configuration) as api_client:
    api_instance = onepanel.core.api.InferenceServiceApi(api_client)

    try:
        ready = False
        while not ready:
            api_response = api_instance.get_inference_service(namespace, model_name)
            ready = api_response.ready
            endpoint = api_response.predict_url
            print('---api_response.predict_url---', endpoint)
            time.sleep(1)
    except ApiException as e:
        print("Exception when calling InferenceServiceApi->get_inference_service_status: %s\n" % e)




headers = {
    'Content-Type': 'application/json',
}

with open('./persons.pkl','rb') as f:
    img_data = pickle.load(f)

data = {
    'instances': [
        {'data': img_data}
    ]
}

headers = {
    'onepanel-access-token': access_token,
    'Content-Type': 'application/json',
}

print('headers', headers)
print('endpoint', endpoint)

r = requests.post(endpoint, headers=headers, data=json.dumps(data))

result = r.json()
print(result)

