Keep-Alive timeout race
=======================

This script demonstrates a race condition that can happen with python-requests
and certain web servers.

The default with Apache httpd 2.4 is KeepAliveTimeout = 5. If you make a request,
wait just the right amount of time, then make another request, the requests
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

An strace of the httpd process shows that httpd is shutting down the connection
just before it receives the new request.

    11935 02:23:33 poll([{fd=15, events=POLLIN}], 1, 5000 <unfinished ...>
    11935 02:23:38 <... poll resumed> )     = 0 (Timeout) <5.005165>
    11935 02:23:38 shutdown(15, SHUT_WR)    = 0 <0.000195>
    11935 02:23:38 poll([{fd=15, events=POLLIN}], 1, 2000) = 1 ([{fd=15, revents=POLLIN}]) <0.000122>
    11935 02:23:38 read(15, "GET /koji-static/debug.css HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nUser-Agent: timeout-race/4\r\n\r\n", 512) = 153 <0.000073>
    11935 02:23:38 poll([{fd=15, events=POLLIN}], 1, 2000) = 1 ([{fd=15, revents=POLLIN|POLLHUP}]) <0.000030>
    11935 02:23:38 read(15, "", 512)        = 0 <0.000053>
    11935 02:23:38 close(15)                = 0 <0.000092>
    11935 02:23:38 read(7, 0x7ffefc539c3f, 1) = -1 EAGAIN (Resource temporarily unavailable) <0.000041>
    11935 02:23:38 semop(5013504, [{0, -1, SEM_UNDO}], 1 <unfinished ...>

Judging from comments in [issue 3456](https://github.com/kennethreitz/requests/issues/3458),
this may not be something that requests can reasonably fix. Possibly this is
a weakness in the http/1.1 specification.

> The server has not read from the socket layer yet, correct. However, the requests side of the connection cannot know that: from our perspective, our (blocking) writes have succeeded, which means that we have transferred data to the server. We are now expecting a response.

> In practice, we like to leave that choice up to our users, who are better placed to decide what to retry than we are.

See also
* https://github.com/kennethreitz/requests/issues/2364
* https://github.com/kennethreitz/requests/issues/3458
