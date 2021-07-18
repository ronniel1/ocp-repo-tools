#!/bin/env python

from git import Repo
import os
import subprocess
from collections import Counter
import argparse


repo = Repo(os.getcwd(), search_parent_directories=True)
DIRS_TO_IGNORE = ["RCS", ".git"]
COMMITERS_TO_IGNORE = [
    "Raz Regev",
    "Raz",
    "Priyanka Jiandani",
    "Sudarshan Acharya",
    "Amador Pahim",
    "Rewant Soni",
    "Dominik Holler",
    "Angus Salkeld",
    "dependabot[bot]",
]



# list of all githubs users gotten using
# https://beaudry-maxime.medium.com/export-the-github-statistics-of-your-organization-contributors-19a40bbe2784
GIT_TO_GITHUB_MAP = {
    "Antoni Segura Puimedon": "celebdor",
    "Avishay Traeger": "avishayt",
    "Daniel Erez": "danielerez",
    "David Zager": "djzager",
    "Elior Erez": "eliorerz",
    "Eran Cohen": "eranco74",
    "Flavio Percoco": "flaper87",
    "Fred Rolland": "rollandf",
    "gamli75": "gamli75",
    "Igal Tsoiref": "tsorya",
    "Jakub Dzon": "jakub-dzon",
    "Jordi Gil": "jordigilh",
    "Juan Manuel Parrilla Madrid": "jparrill",
    "Liat Gamliel": "gamli75",
    "Lisa Rashidi-Ranjbar": "lranjbar",
    "Mario Vázquez": "mvazquezc",
    "Mateusz Kowalski": "mkowalski",
    "Michael Filanov": "filanov",
    "Michael Hrivnak": "mhrivnak",
    "Michael Levy": "michaellevy101",
    "Moti Asayag": "masayag",
    "Nick Carboni": "carbonin",
    "Nir Magnezi": "nmagnezi",
    "Omer Tuchfeld": "omertuc",
    "Ondra Machacek": "machacekondra",
    "Ori Amizur": "ori-amizur",
    "Osher Coehn": "oshercc",
    "osher cohen": "oshercc",
    "Osher Cohen": "oshercc",
    "Osher De Paz": "osherdp",
    "Pawan Pinjarkar": "pawanpinjarkar",
    "Piotr Kliczewski": "pkliczewski",
    "Ravid Brown": "ravidbro",
    "Richard Su": "rwsu",
    "Ronnie Lazar": "ronniel1",
    "Rom Freiman": "romfreiman",
    "Sagi Dayan": "sagidayan",
    "slavie": "slaviered",
    "Vitaliy Emporopulo": "empovit",
    "Vitaly": "empovit",
    "Yevgeny Shnaidman": "yevgeny-shnaidman",
    "Yoni Bettan": "ybettan",
    "Yuval Goldberg": "YuviGold"
}



def get_committers_for_file(file_name):
    blamers = Counter()
    for commit, lines in repo.blame('HEAD', file_name):
        blamers[commit.author.name] += len(lines)

    return blamers


def committer_to_github_user(committer):
    try:
        return GIT_TO_GITHUB_MAP[committer]
    except:
        if committer not in COMMITERS_TO_IGNORE:
            print("Git committer {} not found in GIT_TO_GITHUB_MAP".format(committer))
        return None


def handle_dir(args, path):
    print("Handling {}".format(path))
    res = subprocess.check_output('git ls-files | grep -v "\/" || true', shell=True, cwd=path)
    files = res.decode('utf-8')
    blamers = Counter()
    for f in files.split('\n'):
        if len(f) == 0:
            continue
        file_blamers = get_committers_for_file(os.path.join(path, f))
        blamers += file_blamers

    if len(blamers) == 0:
        return
    with open(os.path.join(path, args.output_file_name), "w") as fout:
        for i, b in enumerate(blamers.most_common()):
            if i >= int(args.top_n_committers):
                break
            guser = committer_to_github_user(b[0])
            if guser:
                fout.write(guser+"\n")


def should_handle(path):
    for i in DIRS_TO_IGNORE:
        if i in path:
            return False
    return True


def main(args):
    for root, subdirs, _ in os.walk(os.getcwd(), topdown=True):
        #import ipdb; ipdb.set_trace()
        if not should_handle(root):
            continue
        handle_dir(args, root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--top-n-committers", default=7,
                        help="Top N committers to use")
    parser.add_argument("-o", "--output-file-name", default="OW.txt",
                           help="Name of file to create in each directory")
    args = parser.parse_args()
    print(args)
    main(args)


