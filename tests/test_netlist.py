"""Test netlist utility."""
import unittest
from unittest import mock
import toml
from rfdesigner import netlist
from rfdesigner.components import Generic, Passive


class TestNetlist(unittest.TestCase):
    """Object to test netlist."""

    def test_validate_signal_chain_missing_keys(self):
        """Tests the validate signal chain method with missing data."""
        name = "test"
        system = {}
        self.assertFalse(netlist.validate_signal_chain(name, system))
        system = {"1": {"foo": "bar"}}
        self.assertFalse(netlist.validate_signal_chain(name, system))
        system = {"1": {"type": "foobar"}}
        self.assertFalse(netlist.validate_signal_chain(name, system))

    def test_validate_signal_chain_ok(self):
        """Test the validate signal chain method with good data."""
        name = "test"
        system = {"1": {"type": "generic"}}
        self.assertTrue(netlist.validate_signal_chain(name, system))

    def test_signal_chain_class(self):
        """Test the SignalChain class."""
        system = {"1": {"type": "generic"}, "2": {"type": "passive"}}
        chain = netlist.SignalChain("foobar", system)
        self.assertEqual(chain.name, "foobar")
        self.assertEqual(chain.system[0].__class__, Generic)
        self.assertEqual(chain.system[1].__class__, Passive)

    def test_parse_netlist_missing_file(self):
        """Test netlist parsing failure on missing file."""
        self.assertEqual(netlist.parse_netlist("/foo/bar"), None)

    @mock.patch("rfdesigner.netlist.toml.load", side_effect=toml.loads)
    def test_parse_netlist_bad_data(self, mock_toml):
        """Test empty dict on bad toml data."""
        toml_data = ""
        self.assertEqual(netlist.parse_netlist(toml_data), None)
