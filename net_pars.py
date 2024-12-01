import xml.etree.ElementTree as ET

class Interface:
    def __init__(self, id, name, description, mac_address, status):
        self.id = id
        self.name = name
        self.description = description
        self.mac_address = mac_address
        self.status = status

    def to_xml(self):
        interface_elem = ET.Element("Interface")
        ET.SubElement(interface_elem, "Id").text = self.id
        ET.SubElement(interface_elem, "Name").text = self.name
        ET.SubElement(interface_elem, "Description").text = self.description or "N/A"
        ET.SubElement(interface_elem, "MacAddress").text = self.mac_address
        ET.SubElement(interface_elem, "Status").text = self.status
        return interface_elem

def get_input(prompt="Введите данные для парсинга (введите пустую строку, чтобы завершить анализ): "):
    print(prompt)
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)

def parse_device(output):
    status_arr = []
    interfaces = []
    current_description = None
    for line in output.splitlines():
        line = line.strip()
        parts = line.split(" ")
        if ";;;" in line:
            current_description = line.split(";;;", 1)[1].strip()
        if line and not line.startswith("Flags"):
            if line and not line.startswith("Flags"):
                parts = line.split(" ")
                flags = parts[1]
                if flags == 'RS' or flags == 'R':
                    status = "up"
                elif flags == 'X' or flags == 'XS':
                    status = "down"
            attributes = {}
            for part in parts[0:]:
                if "=" in part:
                    key, value = part.split("=", 1)
                    attributes[key] = value.strip('"')
            interface = Interface(
                id=attributes.get("name", ""),
                name=attributes.get("default-name", ""),
                description=current_description,
                mac_address=attributes.get("mac-address", ""),
                status=status,
            )
            if interface.id == '' and interface.name == '' and interface.mac_address == '':
                continue
            else:
                interfaces.append(interface)
                current_description = None
    return interfaces


def interfaces_to_xml(interfaces):
    root = ET.Element("Interfaces")
    for interface in interfaces:
        root.append(interface.to_xml())
    return ET.tostring(root, encoding="unicode")


if __name__ == "__main__":
    device_output = get_input()
    interfaces = parse_device(device_output)
    xml_output = interfaces_to_xml(interfaces)
    print(xml_output)