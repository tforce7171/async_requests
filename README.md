# async_requests

**async_requests** lets you easily make lot of http requests asyncronusly.

```python
>>> import async_requests
>>> urls = ["https://www.google.com/"]
>>> results = async_requests.get(urls)
>>> results
[<ClientResponse(https://www.google.com/) [200 OK]> ... ]
## Installing async_requests

```console
$ python -m pip install git+https://github.com/tforce7171/async_requests.git
```
