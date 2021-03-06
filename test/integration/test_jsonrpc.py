import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from dashd import DashDaemon
from dash_config import DashConfig


def test_dashd():
    config_text = DashConfig.slurp_config_file(config.dash_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000ee6635b617e6b850ba638411c956bc5e0b977c2aa466a2116b4b767599c'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000004d72c95dada076575d05dddfb8be794c5ff8e6fa983e18b509995a03740'

    creds = DashConfig.get_rpc_creds(config_text, network)
    dashd = DashDaemon(**creds)
    assert dashd.rpc_command is not None

    assert hasattr(dashd, 'rpc_connection')

    # LUSO testnet block 0 hash == 000004d72c95dada076575d05dddfb8be794c5ff8e6fa983e18b509995a03740
    # test commands without arguments
    info = dashd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert dashd.rpc_command('getblockhash', 0) == genesis_hash
