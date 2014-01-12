#! /usr/bin/env python
import sys
from functools import partial
from collections import defaultdict

from fabric.api import run, env, sudo, task, runs_once

from cloth.utils import instances, use


module = sys.modules[__name__]
env.nodes = []
env.roledefs = defaultdict(list)

NODE_ENVS = {
    'preview': '^preview-',
    'production': '^production-'
}


def set_node_envs(node_envs=NODE_ENVS):
    for node_env in node_envs:
        def _env_nodes(k):
            nodes(node_envs.get(k))

        ptask = partial(_env_nodes, node_env)
        ptask.__doc__ = "{0} nodes".format(node_env.capitalize())

        setattr(module, node_env, task(name=node_env)(ptask))


@task
def all():
    "All nodes"
    for node in instances():
        use(node)


@task
def nodes(exp):
    "Select nodes based on a regular expression"
    for node in instances(exp):
        use(node)


@task
@runs_once
def list():
    "List EC2 name and public and private ip address"
    for node in env.nodes:
        print "{0} ({1}, {2})".format(node.tags["Name"],
                                      node.ip_address,
                                      node.private_ip_address)


@task
def uptime():
    "Show uptime and load"
    run('uptime')


@task
def free():
    "Show memory stats"
    run('free')


@task
def updates():
    "Show package counts needing updates"
    run("cat /var/lib/update-notifier/updates-available")


@task
def upgrade():
    "Upgrade packages with apt-get"
    sudo("apt-get update; apt-get upgrade -y")
