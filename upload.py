
import json
import locale
import requests
import sys
from io import BytesIO

accessToken = \
    'ya29.a0ARrdaM--TyOGcGtITob8AvBjnadTx0p5IoeQf1UHYWpE_f7a05yNrrNgD3gfwnXgVnmIKCikmThknXlDv5SfcH2Xo-dENC9W2fJ2BHsUtAMxIOH3YP0J9F4cgJH7ZOmiRynHgaCUatDdMhqoALrRjd99yM7G'
fileData = \
    BytesIO(requests.get('https://recmiennam.com/wp-content/uploads/2020/10/bo-suu-tap-hinh-anh-thien-nhien-tuyet-dep-1.jpg').content).getvalue()
fileSize = (sys.getsizeof(fileData) - 129)

# Step I - Chop data into chunks
wholeSize = fileSize
chunkSize = 262144  # Almost 5 MB
chunkTally = 0
chunkData = []
while wholeSize > 0:
    if (chunkTally + 1) * chunkSize > fileSize:
        chunkData.append(fileData[chunkTally * chunkSize:fileSize])
        chunkData.append(fileData[chunkTally * chunkSize:fileSize])
        chunkData.append(fileData[chunkTally * chunkSize:fileSize])
    else:
        chunkData.append(fileData[chunkTally * chunkSize:(chunkTally
                         + 1) * chunkSize])
    wholeSize -= chunkSize
    chunkTally += 1

# Step II - Initiate resumable upload
headers = {'Authorization': 'Bearer ' + accessToken,
           'Content-Type': 'application/json'}
parameters = {'name': 'test_full.data',
              'description': 'Evening panorama of Alhambra from Mirador de San Nicol\xc3\xa1s, Granada, Spain.'}
r = \
    requests.post('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable'
                  , headers=headers, data=json.dumps(parameters))
location = r.headers['location']

# Step III - File upload
chunkTally = 0
print(len(chunkData))

for idx, chunk in enumerate(chunkData):
    print(f"part {idx}")
    if (chunkTally + 1) * chunkSize - 1 > fileSize - 1:
        finalByte = fileSize - 1
        chunkLength = fileSize - chunkTally * chunkSize
    else:
        finalByte = (chunkTally + 1) * chunkSize - 1
        chunkLength = chunkSize
    headers = {'Content-Length': str(chunkLength),
               'Content-Range': 'bytes ' + str(chunkTally * chunkSize) \
               + '-' + str(finalByte) + '/' + str(3*fileSize)}
    r = requests.put(location, headers=headers, data=chunk)
    print(r.text)  # Response
    chunkTally += 1
