import xml.etree.ElementTree as ET

psatsim = ET.Element("psatsim")
count = 0

# Loop to generate <general> blocks
for superscalar_val in range(1, 17): #1-16
    for functional_units_val in range(1, 9): #1-8
        for reservation_val in range(1, 9): #1-8
            for reorder_buffer_val in range(1, 513): #1-512
                # Only use f area is less than 60 mm2
                area = (
                     (0.065 * (functional_units_val*4) * reservation_val) + 
                     2.0 * functional_units_val + 
                     3.5 * functional_units_val +
                     1.5 * functional_units_val +
                     3.0 * functional_units_val +
                     0.04 * reorder_buffer_val * superscalar_val + 
                     0.035 * reorder_buffer_val
                     ) 
                if area <= 60:
                    count += 1
                    config = ET.SubElement(psatsim, "config", name="Case" + str(count))
                    general = ET.SubElement(config, "general", {
                        "superscalar": str(superscalar_val),
                        "rename": str(reorder_buffer_val),
                        "reorder": str(reorder_buffer_val),
                        "rsb_architecture": "distributed",
                        "rs_per_rsb": str(reservation_val),
                        "speculative": "true",
                        "speculation_accuracy": "0.960",
                        "separate_dispatch": "true",
                        "seed": "0",
                        "trace": r"C:\Program Files (x86)\PSATSim\Traces\mpeg2e.tra",
                        "output": r"C:\Users\lruiz\Documents\ECE533\result.xml",
                        "vdd": "2.2",
                        "frequency": "600"
                    })
                    execution = ET.SubElement(config, "execution", {
                        "architecture": "standard",
                        "integer": str(functional_units_val),
                        "floating": str(functional_units_val),
                        "branch": str(functional_units_val),
                        "memory": str(functional_units_val)
                    })
                    memory = ET.SubElement(config, "memory", {
                                            "architecture": "l2"
                                        })
                    ET.SubElement(memory, "system", {"latency": "5"})
                    ET.SubElement(memory, "l1_code", {"hitrate": "0.970", "latency": "1"})
                    ET.SubElement(memory, "l1_data", {"hitrate": "0.970", "latency": "1"})
                    ET.SubElement(memory, "l2", {"hitrate": "0.940", "latency": "3"})
print(count)

# Save XML
tree = ET.ElementTree(psatsim)
tree.write("generated.xml", encoding='utf-8', xml_declaration=True)

import xml.dom.minidom

# Write raw XML first
tree = ET.ElementTree(psatsim)
tree.write("generated.xml", encoding='utf-8', xml_declaration=True)

# Pretty print XML
with open("generated.xml", "r", encoding='utf-8') as f:
    xml_string = f.read()

pretty_xml = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="    ")

with open("generated.xml", "w", encoding='utf-8') as f:
    f.write(pretty_xml)
