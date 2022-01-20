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

## create_purls_from_csv.py
The `create_purls_from_csv.py` script can be used to create PURLs in batches, where the values for the PURL `domain`, `id`, and `target` is specified by each row of the `csv`.

Similar to above, you pass values for `--host`, `--username`, and `--password` to the command, in addition to specifying a well-formatted `--purl_csv` file for the script to iterate over and create new PURLs. Further, the script will output a new `csv.results` file that contains the original `domain`, `id`, and `target` values for each row in addition to new columns for `purl` (what the script mints) and `status` (`success` or `failure`). If the script fails at a PURL, it will perform a `sys.exit`, print a message to the `stdout`, and the new csv will be written up to that point.

## formatting `--purl_csv` and example
Your `--purl_csv` file should look something like this:

domain,id,target
purl_domain,purl_id_01,https://www.python.org/
purl_domain,purl_id_02,https://github.com/
purl_domain,purl_id_03,https://www.wikipedia.org/

PURL servers don't like spaces or certain special characters (see `create_purls_from_csv.py` for a list of these) in the `id` field, so avoid these in your `.csv` to help the script run more smoothly. Generally, sticking to basic alphanumeric characters and dashes (`-`) or underscores (`_`) is a good guideline to follow. Furthermore, the `domain` must be created directly on the PURL server by an admin before minting PURLs within that domain, so be sure to do this before initiating a batch job. 
