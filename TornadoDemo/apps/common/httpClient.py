#!/usr/bin/env python
# encoding: utf-8
import asyncio
import binascii
import six
import os
from io import BytesIO
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class HttpClient(object):
    def __init__(self):
        self.sess = AsyncHTTPClient()

    async def get(self, url="", data=None):
        params = "" if data is None else "&".join("=".join(kv) for kv in data.items())
        request = HTTPRequest(url=url + "?" + params, method="GET")
        try:
            resp = await self.sess.fetch(request)
            content = resp.body.decode("utf-8")
            return content
        except Exception as e:
            print("Error: %s" % e)

    async def post(self, url=None, data=None, files=None):
        if files is not None:
            content_type, body = self.encode_multipart_formdata(data=data, files=files)
            headers = {"Content-Type": content_type, 'content-length': str(len(body))}
        else:
            body = {} if data is None else "&".join("=".join([str(k), str(v)]) for k, v in data.items())
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request = HTTPRequest(url=url, method="POST", headers=headers, body=body)
        try:
            resp = await self.sess.fetch(request)
            content = resp.body.decode("utf-8")
            return content
        except Exception as e:
            print("Error: %s" % e)
            return

    def choose_boundary(self):
        """
        Our embarrassingly-simple replacement for mimetools.choose_boundary.
        """
        boundary = binascii.hexlify(os.urandom(16))
        if six.PY3:
            boundary = boundary.decode('ascii')
        return boundary

    def encode_multipart_formdata(self, data=None, files=None):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be
        uploaded as files.
        Return (content_type, body) ready for httplib.HTTP instance
        """
        body = BytesIO()
        boundary = self.choose_boundary()
        for key, value in data.items():
            body.write(('--%s\r\n' % boundary).encode(encoding="utf-8"))
            body.write(('Content-Disposition:form-data;name="%s"\r\n' % key).encode(encoding="utf-8"))
            body.write('\r\n'.encode(encoding="utf-8"))
            if isinstance(value, int):
                value = str(value)
            body.write(('%s\r\n' % value).encode(encoding="utf-8"))

        for key, value in files.items():
            body.write(('--%s\r\n' % boundary).encode(encoding="utf-8"))
            body.write(('Content-Disposition:form-data;name="file";filename="%s"\r\n' % key).encode(encoding="utf-8"))
            body.write('\r\n'.encode(encoding="utf-8"))
            body.write(value)
            body.write('\r\n'.encode(encoding="utf-8"))

        body.write(('--%s--\r\n' % boundary).encode(encoding="utf-8"))
        content_type = 'multipart/form-data;boundary=%s' % boundary
        return content_type, body.getvalue()


zd_requests = HttpClient()


async def test_get():
    data = {"show_env": '1'}
    resp = await zd_requests.get(url="https://httpbin.org/get", data=data)
    print(resp)


async def test_post():
    data = {"show_env": '1'}
    resp = await zd_requests.post(url="https://httpbin.org/post", data=data)
    print(resp)


async def test_file_upload():
    data = {"subpath": "", "unformat": "0"}
    files = {
        "1.mp3": open("db.py", "rb").read()
    }
    request_url = "http://www.baidu.com"
    resp = await zd_requests.post(url=request_url, data=data, files=files)
    print(str(resp.body.decode(encoding="utf-8")))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_post())
