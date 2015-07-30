#! /usr/bin/env python
# coding=utf-8

import argparse
import os
import subprocess

# Third Party
import git


class GitPriorityMerge(object):

    @classmethod
    def get_repo_path(cls):
        # Taken from Git up
        abspath = os.path.abspath('.')
        git_dir = os.path.join(abspath, '.git')

        if os.path.exists(git_dir) and os.path.isdir(git_dir):
            return abspath

        return subprocess.check_output('git rev-parse --show-toplevel', shell=True).replace('\n', '')

    def __init__(self, base_branch=None, branch_file=None, *branches):
        try:
            self.repo = git.Repo(self.__class__.get_repo_path(), odbt=git.GitCmdObjectDB)
        except subprocess.CalledProcessError:
            # TODO: Change this to a better error.
            raise TypeError('Not in a git repository')

        self.base_branch = base_branch or self.repo.active_branch.name
        self.branch_file = branch_file or branches
        try:
            self.remote = self.repo.remotes[0]
        except IndexError:
            raise IndexError('No remotes were found')
        '''
        if not self.branch_file or self.branches:
            raise ValueError('Need either a file of branch names or a list of branches')
        '''

    def fetch(self):
        print self.repo.git.fetch(all=True)

    @property
    def branches(self):
        return self._branches if hasattr(self, '_branches') else []

    @branches.setter
    def branches(self, branches=None):
        self._branches = []
        # File name
        if isinstance(branches, str):
            with open(braches, 'r') as f:
                self._branches = [l.strip() for l in f]
        elif isinstance(branches, list):
            self._branches = branches

    def refresh_branches(self):
        remote_name = self.remote.name
        branch_names = [b.name for b in self.repo.branches]
        remote_branch_names = [b.name for b in self.remote.refs]
        for b in branch_names:
            if
        pass



def parse_args():
    parser = argparse.ArgumentParser(description='Merge several branches in order')
    parser.add_argument('-b', '--base', default=None, help='Branch to use as base.')
    parser.add_argument('-f', '--file', default=None, help='File for branch names.')
    parser.add_argument('--branches', nargs='*')
    return parser.parse_args()


def run():
    args_namespace = parse_args()


if __name__ == '__main__':
    print 'I GOT HERE'
    run()
