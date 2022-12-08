import json
import sys
import unittest
from http.client import HTTPResponse
from urllib import request


class WebServiceTest(unittest.TestCase):

    def test_post_run(self):

        try:
            req = request.Request('http://localhost:5000/check', method='GET')
            self.assertEqual(request.urlopen(req).status, 200)
        except Exception:
            print('Connection refused! Please check if the server is running at http://localhost:5000/check',
                  file=sys.stderr)
            sys.exit(1)

        data = {'command': 'echo hello'}
        data = str(json.dumps(data)).encode('utf-8')
        req = request.Request('http://localhost:5000/run', data=data, method='POST',
                              headers={'Content-Type': 'application/json'})
        resp: HTTPResponse = request.urlopen(req)
        self.assertEqual(resp.status, 200)
        self.assertEqual(
            json.loads(resp.read().decode('UTF-8')),
            {"return_code": 0, 'stderr': '', 'stdout': 'hello\n'}
        )


if __name__ == '__main__':
    unittest.main()
