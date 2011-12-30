ratelimitcache for Flask
=========================
By Simon Willison - http://simonwillison.net/

Ported to Flask by Casey Link - http://binaryelysium.com

A rate limiter for [Flask][flask] that uses the [Werkzeug Cache API][fc] with no requirement for a persistent data store.

More information (for the original django version) at http://simonwillison.net/2009/Jan/7/ratelimitcache/

Installation:

    Place the ratelimitcache.py on your Python path.

    Configure your cache settings. For best results, use the memcached
    backend - the other backends do not provide an atomic counter increment
    and so may suffer from less effective limiting due to race conditions.

    Cache documentation: [http://werkzeug.pocoo.org/docs/contrib/cache/][fc]

Demo:
    cd demo/
    python hello.py

    Now browse to:
        http://localhost:5000
        http://localhost:5000/api/minute

Basic usage (max 20 requests every 3 minutes):

    from ratelimitcache import ratelimit
    from werkzeug.contrib.cache import SimpleCache

    cache = SimpleCache()

    @app.route('/api/something')
    @ratelimit(cache = cache, minutes = 3, requests = 20)
    def do_something():
        # ...
        return render_template( ... )

This module is also compatible with the [Flask-Cache][fc2] extension. Simply
pass the internal `cache` object:

    from flaskext.cache import Cache

    cache = Cache(app)

    @ratelimit(cache = cache.cache, minutes = 3, requests = 20)
    def do_something():
        # ...
        return render_template( ... )

Protecting a login form, i.e rate limit on IP address and attempted username:
**This example is for django** (TODO: port to flask)

    from ratelimitcache import ratelimit_post

    @ratelimit_post(cache, minutes = 3, requests = 10, key_field = 'username')
    def login(request):
        # ...
        return HttpResponse('...')

Custom behaviour, e.g. logging when the rate limit condition fails:
**This example is for django** (TODO: port to flask)

    from ratelimitcache import ratelimit
    from my_logging_app.models import Log
    import datetime, pprint

    class ratelimit_with_logging(ratelimit):
        def disallowed(self, request):
            Log.objects.create(
                ip_address = request.META.get('REMOTE_ADDR'),
                path = request.path,
                counters = pprint.pformat(
                    self.get_counters(reqest)
                ),
                created = datetime.datetime.now()
            )
            return HttpResponseForbidden('Rate limit exceeded')

    @ratelimit_with_logging(minutes = 3, requests = 20)
    def myview(request):
        # ...
        return HttpResponse('...')


[flask]: http://flask.pocoo.org/
[fc]: http://werkzeug.pocoo.org/docs/contrib/cache/
[fc2]: http://packages.python.org/Flask-Cache/
