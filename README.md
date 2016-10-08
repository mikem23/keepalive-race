Keep-Alive timeout race
=======================

This script demonstrates a race condition that can happen with python-requests
and certain web servers.

The default with Apache httpd 2.4 is KeepAliveTimeout = 5. If you make a request,
wait just the right amount of time, then make another request, then requests
module may opt to reuse the connection, but by the time the server gets it
the timeout will have expired.

With at least some versions of Apache httpd, the server will return an empty
response, or at least the client will recieve one. This results in a traceback like

    Traceback (most recent call last):
      File "./test.py", line 38, in <module>
        session.get(url, verify=False, headers=headers)
      File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 487, in get
        return self.request('GET', url, **kwargs)
      File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 475, in request
        resp = self.send(prep, **send_kwargs)
      File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 585, in send
        r = adapter.send(request, **kwargs)
      File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 453, in send
        raise ConnectionError(err, request=request)
    requests.exceptions.ConnectionError: ('Connection aborted.', BadStatusLine("''",))

Usage:

    test.py [--debug] <url> [delay]

Where url is the url to read and delay is the time between requests in seconds
(defaults to 5). If the --debug option is given, then you'll see lots of debug
output.

The more network latency, the easier it is to hit the race. However, even
against a local httpd server, I am able to dial in the delay to hit it
reliably (in my case, about 4.995).

See also
* https://github.com/kennethreitz/requests/issues/2364
