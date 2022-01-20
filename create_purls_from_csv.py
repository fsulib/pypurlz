#!/usr/bin/env python3

import click
import os
from csv import DictReader
from csv import writer
import subprocess
import sys
import csv
import requests

@click.command()
@click.option('--host', help='The PURL server we want to connect to')
@click.option('--username', help='User logging into PURLZ server')
@click.option('--password', help='Password for logging into PURLZ server')
@click.option('--purl_csv', help='CSV file containing domain, id, and target columns to create PURLs')

def exec(host, username, password, purl_csv):
    if host is None:
        sys.exit("Host not provided")
    if username is None:
        sys.exit("Username not specified")
    if password is None:
        sys.exit("Password not provided")
    if purl_csv is None:
        sys.exit("CSV file not provided")

    results = []
    results_header = ["domain", "id", "target", "purl", "status"]
    with open (purl_csv,"r") as row_counter:
        reader = csv.reader(row_counter)
        next(reader)
        data = list(reader)
        all_row_count = len(data)
        rowcount = 0
    with open(purl_csv, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            rowcount+= 1
            domain = row['domain']
            id = row['id']
            target = row['target']
            if " " in id:
                print('ID {id} in row {rowcount} contains spaces. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if "#" in id:
                print('ID {id} in row {rowcount} contains special character, #. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if "$" in id:
                print('WARNING: Id {id} in row {rowcount} contains special character, $. This will write a PURL with the wrong ID! Remove the special character.'.format(id=id, rowcount=rowcount+1))
            if "%" in id:
                print('ID {id} in row {rowcount} contains special character, %. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if "^" in id:
                print('ID {id} in row {rowcount} contains special character, ^. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if "&" in id:
                print('ID {id} in row {rowcount} contains special character, &. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if "(" in id:
                print('ID {id} in row {rowcount} contains special character, (. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if ")" in id:
                print('ID {id} in row {rowcount} contains special character, ). It is invalid!'.format(id=id, rowcount=rowcount+1))
            if "<" in id:
                print('ID {id} in row {rowcount} contains special character, <. It is invalid!'.format(id=id, rowcount=rowcount+1))
            if ">" in id:
                print('ID {id} in row {rowcount} contains special character, >. It is invalid!'.format(id=id, rowcount=rowcount+1))
            target_check = requests.get(target)
            if target_check.status_code != 200:
                print('Target is not a valid URL')
            else:
                print('Target is valid URL')
            output = subprocess.check_output("./create_single_purl.py --host {host} --username {username} --password {password} --domain {domain}  --id {id} --target {target}".format(host=host, username=username, password=password, domain=domain, id=id, target=target), shell=True)
            output = output.decode("utf-8").strip().split(' | ')
            results_row = [domain, id, target, output[0], output[1]]
            results.append(results_row)
            with open(purl_csv+".results", 'w') as csvfile:
                csvwriter = writer(csvfile)
                csvwriter.writerow(results_header)
                csvwriter.writerows(results)
            print("{}: {}".format(output[1],output[0]))
            print("PURL ", rowcount, "of", all_row_count)
            if output[1] != "success":
                sys.exit("PURL failed on line {rowcount} of the CSV. ".format(rowcount=rowcount+1) + "Failed PURL is " + output[0])

if __name__ == '__main__':
    exec()
