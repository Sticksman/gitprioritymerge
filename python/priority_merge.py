#! /usr/bin/env python
# coding=utf-8

import argparse
import os
import subprocess

# Third Party
import git


class GitPriorityMerge(object):

    @staticmethod
    def get_repo_path():
        # Taken from Git up
        abspath = os.path.abspath('.')
        git_dir = os.path.join(abspath, '.git')

        if os.path.exists(git_dir) and os.path.isdir(git_dir):
            return abspath

        return subprocess.check_output('git rev-parse --show-toplevel', shell=True).replace('\n', '')

    @staticmethod
    def git_up():
        return subprocess.call('git up', shell=True)


    def __init__(self, base_branch=None, branch_file=None, *branches):
        self.base_branch = base_branch or self.repo.active_branch.name
        self.branches = branch_file or branches

        try:
            self.repo = git.Repo(self.__class__.get_repo_path(), odbt=git.GitCmdObjectDB)
        except subprocess.CalledProcessError:
            # TODO: Change this to a better error.
            raise TypeError('Not in a git repository')

        try:
            self.remote = self.repo.remotes[0]
        except IndexError:
            raise IndexError('No remotes were found')

        if not self.branch_file or self.branches:
            raise ValueError('Need either a file of branch names or a list of branches')

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

    @property
    def base_branch(self):
        return self._base_branch if hasattr(self, '_base_branch') else None

    @base_branch.setter
    def base_branch(self, base_branch):
        self._base_branch = None
        if isinstance(base_branch, git.Head):
            self._base_branch = base_branch
        elif isinstance(base_branch, str):
            try:
                self._base_branch = getattr(self.repo, base_branch)
            except AttributeError:
                raise ValueError('No branch of the name %s' % base_branch)

    def refresh_branches(self):
        branches_to_remove = []
        for b_name in self.branches:
            if not hasattr(self.repo.branches, b_name) and hasattr(self.remote.refs, b_name):
                # Create a local branch that tracks from origin.
                self.repo.create_head(
                    b_name, getattr(self.remote.refs, b_name)
                ).set_tracking_branch(
                    getattr(self.remote.refs, b_name)
                )

            elif not getattr(self.repo.branches, b_name).tracking_branch() and hasattr(self.remote.refs, b.name):
                # Set local branch to track origin.
                getattr(
                    self.repo.branches, b_name
                ).set_tracking_branch(
                    getattr(self.remote.refs, b.name)
                )
            else:
                # Excise these branches.
                branches_to_remove(b_name)

        self.branches = [b for b in self.branches if b not in branches_to_remove]

        ret_val = self.__class__.git_up()
        if ret_val:
            raise Exception('Git up failed')  # Replace with actual exception

        return False

    def merge_branches_in_order(self):
        for b_name in self.branches:
            pass

    def three_way_merge(self, base_branch, new_branch):
        merge_base = self.repo.merge_base(base_branch, new_branch)
        self.repo.index.merge_tree(base_branch, base=merge_base)
        self.repo.index.commit(
            'Merged %s into %s' % (new_branch.name, base_branch.name),
            parent_commits=[new_branch.commit, base_branch.commit]
        )
        base_branch.commit = new_branch.commit
        self.repo.head.reference = base_branch
        # TODO: Merge conflict return False
        return True



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
