#!/usr/bin/env python

import os
import argparse
import shutil
from urllib.parse import urlparse
import certifi
import urllib3

from response_processing import util


def main():
    parser = argparse.ArgumentParser("download all samples references in dumpfile")
    parser.add_argument("dumpfile", help="The output of \"flask dumpdb --outfile=dump.json\"")
    parser.add_argument('outfolder', help='output folder to put samples in')

    args = parser.parse_args()

    responses_by_url = util.load_by_url(args.dumpfile)
    final_responses_by_url = util.get_final_responses(responses_by_url)

    # verify TLS certificates (older urllib3 versions don't by default)
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    for sample_url, final_responses in final_responses_by_url.items():
        o = urlparse(sample_url)
        sample_name = os.path.split(o.path)[-1]
        outfile = os.path.join(args.outfolder, sample_name)

        if os.path.isfile(outfile):
            print("skipping", outfile)
            continue

        print(sample_url, '->', outfile)

        with http.request('GET', sample_url, preload_content=False) as r, open(outfile, 'wb') as out_file:
            shutil.copyfileobj(r, out_file)


if __name__ == '__main__':
    main()
