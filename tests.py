import unittest
from xml.etree import ElementTree as ET
from net_pars import parse_device, interfaces_to_xml

class TestDeviceParsing(unittest.TestCase):

    def setUp(self):
        self.device_output = """
        Flags: X - disabled, R - running; S - slave
        0 RS ;;; LAN
          name="LAN" default-name="ether2" mtu=1500 mac-address=50:00:00:31:00:01 orig-mac-address=50:00:00:31:00:01 arp=enabled
        1 R  name="ether1" default-name="ether1" mtu=1500 mac-address=50:00:00:31:00:00 orig-mac-address=50:00:00:31:00:00 arp=enabled
        2 RS name="ether3" default-name="ether3" mtu=1500 mac-address=50:00:00:31:00:02 orig-mac-address=50:00:00:31:00:02 arp=proxy-arp
        3 X  ;;; bla bla description for the ether4 interface
          name="ether4" default-name="ether4" mtu=1500 mac-address=50:00:00:31:00:03 orig-mac-address=50:00:00:31:00:03 arp=enabled
        """
    def test_parse_devicet(self):
        interfaces = parse_device(self.device_output)
        self.assertEqual(len(interfaces), 4)
        self.assertEqual(interfaces[0].id, "LAN")
        self.assertEqual(interfaces[0].description, "LAN")
        self.assertEqual(interfaces[0].mac_address, "50:00:00:31:00:01")
        self.assertEqual(interfaces[0].status, "up")

        self.assertEqual(interfaces[3].id, "ether4")
        self.assertEqual(interfaces[3].description, "bla bla description for the ether4 interface")
        self.assertEqual(interfaces[3].mac_address, "50:00:00:31:00:03")
        self.assertEqual(interfaces[3].status, "down")

    def test_serialize_interfaces_to_xml(self):
        interfaces = parse_device(self.device_output)
        xml_output = interfaces_to_xml(interfaces)
        root = ET.fromstring(xml_output)
        self.assertEqual(root.tag, "Interfaces")
        self.assertEqual(len(root.findall("Interface")), 4)
        first_interface = root.find("Interface")
        self.assertEqual(first_interface.find("Id").text, "LAN")
        self.assertEqual(first_interface.find("MacAddress").text, "50:00:00:31:00:01")
        self.assertEqual(first_interface.find("Status").text, "up")


if __name__ == "__main__":
    unittest.main()
