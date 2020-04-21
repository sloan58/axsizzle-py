<p align="center">
  <b>AxSizzle</b><br>
</p>
<hr>

## Use Case Description

This package provides a thin wrapper around the Cisco Unified Communications Manager (UCM) AXL API library. The UCM AXL API provides an RPC style API to programatically perform CRUD operations on the UCM administration database.

AxSizzle takes away a bit of the hassle with setting up a SOAP client and importing the WSDL by providing an interface to build the request details dynamically. After you specify the UCM version, API method and request body details, the SOAP headers and XML for any API request will be built for you.

## Installation

For now, please clone this repo and import the AxSizzle class.

```
# (WIP)
# pip install axsizzle
```

## Configuration and Usage

You'll need to import the package and create an instance, passing in an object that specifies your UCM details. I've included some examples below to get you started.

## Usage

Below is an example of importing the package and configuring the client.

```python
# Import the package
from AxSizzle import AxSizzle

# Create a Cisco UCM object
# with the required properties
ucm = {
  'ip': '10.1.10.1',
  'username': 'Administrator',
  'password': 'supersecret',
  'version': '12.5',
}

# Create the AXL wrapper client
client = new AxSizzle(ucm)
```

Each API request needs a dictionary that specifies two properties:

- method: The AXL API method to call
- body: The API body in dictionary format

### Get Requests

```python
message = {
  'method': 'getPhone',
  'body': {
    'name': 'SEP001D452CDDB7',
  },
}
```

### Update Requests

```python
message = {
  'method': 'updatePhone',
  'body': {
    'name': 'SEP001D452CDDB1',
    'description': 'Hey, this is a new description!',
  },
}
```

### List Requests

`searchCriteria` and `returnedTags` can take multiple options so make sure you use a list type.

```python
message = {
  'method': 'listPhone',
  'body': {
    'searchCriteria': [{ 'name': '%' }],
    'returnedTags': [{ 'name': '', 'description': '' }],
  }
}
```

### Remove Requests

```python
message = {
  'method': 'removePhone',
  'body': {
    'name': 'SEP123123123123',
  }
}
```

### SQL Requests

```python
message = {
  'method': 'executeSQLQuery',
  'body': {
    'sql': 'SELECT name FROM device',
  }
}
```

### Sending Requests (full example)

```python
# Call the API and log the ouput
import sys
from AxSizzle import AxSizzle

ucm = {
    'ip': '10.1.10.1',
    'username': 'Administrator',
    'password': 'supersecret',
    'version': '12.5'
}

client = AxSizzle(ucm)

message = {
    'method': 'listPhone',
    'body': {
        'searchCriteria': [{'name': '%'}],
        'returnedTags': [{'name': '', 'description': ''}],
    }
}

response = client.callApi(message)

if 'error' in response:
    print(response['error'])
    sys.exit()
else:
    for row in response['phone']:
        print(row['name'])

```

## Todo

- Handle throttle responses

## Author(s)

This project was written and maintained by the following individuals:

- [Marty Sloan](https://github.com/sloan58)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
