#!/usr/bin/env python3

import click
import requests
import sys

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
        registration_request = session.post(host + '/admin/purl/' + domain + '/' + id  + '?target=' + target + '&type=' + purl_type + '&maintainers=' + maintainer)
        validate_purl = requests.get(host + '/' + domain + '/' + id)
        if validate_purl.url == target:
            print(host + '/' + domain + '/' + id + " | success")
        else:
            print(host + '/' + domain + '/' + id + " | failure")

if __name__ == '__main__':
    exec()
