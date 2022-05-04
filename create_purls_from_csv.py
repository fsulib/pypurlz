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
        validity_rowcount = 0
        rowcount = 0
    with open(purl_csv, "r") as csv_validity_check:
        csv_scan = DictReader(csv_validity_check)
        validity_errors = []
        illegal_chars = [' ','#','$','%','^','&','(',')','<','>']
        illegal_chars_set = set(illegal_chars)
        for row in csv_scan:
            validity_rowcount+=1
            purl_id = row['id']
            purl_id_set = set(purl_id)
            detected_illegal_chars = illegal_chars_set.intersection(purl_id_set)
            if len(detected_illegal_chars) != 0:
              detected_illegal_chars_string = ''
              for num, char in enumerate(detected_illegal_chars, start=1):
                if num == 1:
                  pad = ''
                  plural = ''
                else:
                  pad = ', '
                  plural = 's'
                detected_illegal_chars_string = detected_illegal_chars_string + pad + char
              validity_errors.append('Line {line}: Contains illegal character{plural} {characters}'.format(line = validity_rowcount + 1, plural = plural, characters = detected_illegal_chars_string))
    if len(validity_errors) > 0:
      print("The following validity errors were detected in {csv}:".format(csv = purl_csv))
      for error in validity_errors:
        print(error)
      sys.exit()

    with open(purl_csv, 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            domain = row['domain']
            id = row['id']
            target = row['target']
            rowcount += 1
            target_check = requests.get(target)
            if target_check.status_code != 200:
                print('Target is not a valid URL')
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
