#!/usr/bin/env python3

import click
import requests
import sys
from urllib.parse import urlparse

@click.command()
@click.option('--host', help='The PURLZ server we want to connect to')
@click.option('--username', help='User logging into PURLZ server')
@click.option('--password', help='Password for logging into PURLZ server')
@click.option('--domain', help='Domain of PURL we want to create with no leading slash')
@click.option('--id', help='ID of the PURL we want to create')
@click.option('--target', help='URL we want the PURL we are creating to redirect to')
@click.option('--purl_type', default='302', help='Type of PURL being created. Default is 302')
@click.option('--maintainer', default='admin', help='Usernames responsible for creating and maintaining this PURL. Default is admin')

def exec(host, username, password, domain, id, target, purl_type, maintainer):
    if host is None:
        sys.exit("Host not provided")
    if username is None:
        sys.exit("Username not specified")
    if password is None:
        sys.exit("Password not provided")
    if domain is None:
        sys.exit("Domain not provided")
    if id is None:
        sys.exit("ID not provided")
    if target is None:
        sys.exit("Target URL not provided")

    with requests.Session() as session:
        authentication_request = session.post(host + '/admin/login/login-submit.bsh', data = {'id': username, 'passwd': password})
        if authentication_request.status_code != 200:
            sys.exit("Host PURL server cannot be reached. Check server status and host information and try again.")
        if authentication_request.url == host +'/docs/loginfailure.html':
            sys.exit("Login credentials not valid. Check username and password and try again.")

        purl_status_check = requests.get(host + '/' + domain + '/' + id)
        response_url = purl_status_check.url
        response_path = urlparse(response_url).path
        response_domain =response_url.replace(response_path, '') 

        if purl_status_check.status_code == 404:
            if host == response_domain:
                print("PURL does not exist. Minting new PURL. " + host + '/' + domain + '/' + id + " redirects to " + target)
                session.post(host + '/admin/purl/' + domain + '/' + id  + '?target=' + target + '&type=' + purl_type + '&maintainers=' + maintainer)
            else:
                print("PURL already exists. Updating " + host + '/' + domain + '/' + id + " to redirect to " + target )
                session.put(host + '/admin/purl/' + domain + '/' + id  + '?type=302' + '&seealso=&maintainers=admin' + '&target=' + target)
        if purl_status_check.status_code == 200:
            print("PURL already exists. Updating " + host + '/' + domain + '/' + id + " to redirect to " + target )
            session.put(host + '/admin/purl/' + domain + '/' + id  + '?type=302' + '&seealso=&maintainers=admin' + '&target=' + target)

        redirect = requests.get(host + '/' + domain + '/' + id)
        redirect = redirect.url.rstrip('/')
        print("Target: " + target)
        print("Redirect: " + redirect)
        if redirect == target:
            print(host + '/' + domain + '/' + id + " | success")
        else:
            print(host + '/' + domain + '/' + id + " | failure")

if __name__ == '__main__':
    exec()
