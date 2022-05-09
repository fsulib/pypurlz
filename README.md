# pypurlz
Python tools for working with a PURLZ server

## create_single_purl.py
The `create_single_purl.py` script can be run to mint a single PURL for a digital object. The script requires parameters be passed to it from the CLI. These include:

`--host` (URL of host PURL server)

`--username` (username for logging into the PURL server)

`--password` (password for logging into the PURL server)

`--domain`  (domain of the PURL to be minted)

`--id` (id of the PURL to be minted)

`--target` (complete URL of the target the PURL will point to)

`--purl_type` (kind of PURL being minted, see [PURL documentation](https://purl.archive.org/help) for more information, `default=302`)

`--maintainer` (users responsible for maintaining PURL being minted, `default=admin`)

The status of the script (either `success` or `failure`) will print to the the `stdout` along with the newly minted PURL.

### example script for create_single_purl.py

`./create_single_purl.py --host https://yourfavpurlserver.org --username admin --password XXXX --domain purl_domain --id purl_id_01 --target https://www.python.org/`

This will create the PURL `https://yourfavpurlserver.org/purl_domain/purl_id_01` which will redirect to `https://www.python.org/`

## create_purls_from_csv.py
The `create_purls_from_csv.py` script can be used to create PURLs in batches, where the values for the PURL `domain`, `id`, and `target` is specified by each row of a `csv`.

Similar to above, you pass values for `--host`, `--username`, and `--password` to the command, in addition to specifying a well-formatted `--purl_csv` file for the script to iterate over and create new PURLs. Further, the script will output a new `csv.results` file that contains the original `domain`, `id`, and `target` values for each row in addition to new columns for `purl` (what the script mints) and `status` (`success` or `failure`). If the script fails at a PURL, it will perform a `sys.exit`, print a message to the `stdout`, and the `csv.results` file will be written up to that point.

## formatting guidelines for `--purl_csv`, example `--purl_csv`, and additional tips
Your `--purl_csv` file should look something like this:

domain,id,target<br/>
purl_domain,purl_id_01,https://www.python.org/<br/>
purl_domain,purl_id_02,https://github.com/<br/>
purl_domain,purl_id_03,https://www.wikipedia.org/<br/>

PURL servers don't like spaces or certain special characters in the `id` field (see `create_purls_from_csv.py` for a list of such characters), so avoid these in your `.csv` to help the script run smoothly. Generally, sticking to basic alphanumeric characters and dashes (`-`) or underscores (`_`) is a good guideline to follow. Be sure to double-check your `.csv` before running to ensure no duplicate `id` fields are present, as these duplicates can cause errors in the script and require manual remediation.

Additionally, PURL domains must be created on the server by an admin before minting PURLs within that domain, so be sure to do this before initiating a batch or single jobs.

## using the update scripts
The `update_single_purl.py` and `update_purls_from_csv.py` are intended to be used when updating the _target_ of an already exisiting PURL. 

To use the `update_single_purl.py` script, enter the command the same as instructed above for an exisiting PURL and simply add the new target URL to the command. This will modify the existing PURL to point to the new target URL. 

Simiarly, to use the `update_purls_from_csv.py` script, create a well-formed csv using existing domain/id pairs and place the new target URL on each line of the `.csv` in the `target` field. This will batch-update all PURLs to redirect to new targets. 
