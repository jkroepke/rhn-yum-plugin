#!/usr/bin/python

from yum.plugins import TYPE_CORE
from yum.yumRepo import YumRepository

import os, pickle

requires_api_version = '2.5'
plugin_type = TYPE_CORE

def init_hook(conduit):
    rhnd_data = pickle.load(open("/var/spool/up2date/loginAuth.pkl", "rb"))

    # https://github.com/spacewalkproject/spacewalk/blob/master/client/rhel/yum-rhn-plugin/rhnplugin.py#L298
    rhn_needed_headers = ['X-RHN-Server-Id',
                          'X-RHN-Auth-User-Id',
                          'X-RHN-Auth',
                          'X-RHN-Auth-Server-Time',
                          'X-RHN-Auth-Expire-Offset']

    repos = conduit.getRepos()
    cachedir = conduit.getConf().cachedir

    for repo_item in rhnd_data['loginInfo']['X-RHN-Auth-Channels']:
        repo = YumRepository(repo_item[0])
        repo.baseurl = 'https://%s/XMLRPC/GET-REQ/%s' % (os.environ['SPACEWALK_HOST'], repo_item[0])
        repo.urls = repo.baseurl
        repo.name = repo_item[0]
        repo.basecachedir = cachedir
        repo.keepcache = 0

        repo.enable()

        for header in rhn_needed_headers:
            # https://github.com/spacewalkproject/spacewalk/blob/master/client/rhel/yum-rhn-plugin/rhnplugin.py#L403
            if len(str(rhnd_data['loginInfo'][header])) > 0:
                repo.http_headers[header] = str(rhnd_data['loginInfo'][header])
            else:
                repo.http_headers[header] = "%s\r\nX-libcurl-Empty-Header-Workaround: *" % rhnd_data['loginInfo'][header]
        if not repos.findRepos(repo.id):
            repos.add(repo)
