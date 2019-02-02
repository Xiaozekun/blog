from urllib.parse import urljoin, urlparse
from flask import request, redirect, url_for


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(host_url,target))
    return test_url.scheme in ('http', 'https') and host_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next') and request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            redirect(target)
    return redirect(url_for(default, **kwargs))