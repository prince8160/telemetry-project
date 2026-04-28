import json, unittest, datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)

with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


#  Format 1 → (string location + ms timestamp)
def convertFromFormat1(jsonObject):

    locationParts = jsonObject["location"].split("/")

    result = {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

    return result


#  Format 2 → (ISO timestamp → convert)
def convertFromFormat2(jsonObject):

    dt = datetime.datetime.strptime(
        jsonObject['timestamp'],
        '%Y-%m-%dT%H:%M:%S.%fZ'
    )

    timestamp = round(
        (dt - datetime.datetime(1970, 1, 1)).total_seconds() * 1000
    )

    result = {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': jsonObject['data']
    }

    return result


def main(jsonObject):

    if jsonObject.get('device') is not None:
        return convertFromFormat2(jsonObject)
    else:
        return convertFromFormat1(jsonObject)


class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult)


if __name__ == '__main__':
    unittest.main()