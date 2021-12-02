# -*- mode:python; coding:utf-8; -*-
# author: Mariia Boldyreva <mboldyreva@cloudlinux.com>
# created: 2021-10-28

"""
Script for building Vagrant Boxes.
"""

import sys
import argparse
import logging

from lib.builder import Builder
from lib.hypervisors import get_hypervisor


def init_args_parser() -> argparse.ArgumentParser:
    """
    Command line arguments parser initialization.

    Returns
    -------
    argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description='Cloud Images autobuilder'
    )
    parser.add_argument('--hypervisor', type=str,
                        choices=['VirtualBox', 'KVM', 'VMWare_Desktop', 'HyperV'],
                        help='Hypervisor name')
    parser.add_argument('--stage', type=str,
                        choices=['init', 'build', 'destroy',
                                 'test', 'release'],
                        help='Stage')
    return parser


def setup_logger():
    """
    Setup for logger.
    """
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    log_format = "%(asctime)s %(levelname)-8s [%(threadName)s]: %(message)s"
    formatter = logging.Formatter(log_format, '%y.%m.%d %H:%M:%S')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def main(sys_args):
    """
    Executes stages to build, test and release Vagrant Box.
    """
    args_parser = init_args_parser()
    args = args_parser.parse_args(sys_args)

    setup_logger()
    builder = Builder()
    hypervisor = get_hypervisor(args.hypervisor.lower())

    if args.stage == 'init':
        hypervisor.init_stage(builder)
    elif args.stage == 'build':
        hypervisor.build_stage(builder)
    elif args.stage == 'test':
        hypervisor.test_stage(builder)
    elif args.stage == 'release':
        hypervisor.release_stage(builder)
    elif args.stage == 'destroy':
        hypervisor.teardown_stage()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))