import xml.etree.ElementTree as ET

tree = ET.parse(r"C:\Users\lruiz\Documents\ECE533\project.xml")
root = tree.getroot()

best_ipc = 0
lowest_energy = float("inf")
best_balance_score = 0
best_ipc_variant = best_energy_variant = best_balance_variant = None

for variation in root.findall("variation"):
    general_out = variation.find("general")
    ipc = float(general_out.attrib["ipc"])
    energy = float(general_out.attrib["energy"])

    # Find corresponding config/general for area
    general_config = variation.find(".//config/general")
    execution = variation.find(".//config/execution")

    S = int(general_config.attrib["superscalar"])
    NRB = int(general_config.attrib["reorder"])  # same as rename
    NRS = int(general_config.attrib["rs_per_rsb"])

    FI = int(execution.attrib["integer"])
    FFP = int(execution.attrib["floating"])
    FB = int(execution.attrib["branch"])
    FM = int(execution.attrib["memory"])

    area = (
        0.065 * (FI + FFP + FB + FM) * NRS +
        2.0 * FI +
        3.5 * FFP +
        1.5 * FB +
        3.0 * FM +
        0.04 * NRB * S +
        0.035 * NRB
    )

    # Compute balance score (IPC / (energy * area))
    balance_score = ipc / (energy * area)

    if ipc > best_ipc:
        best_ipc = ipc
        best_ipc_variant = variation

    if energy < lowest_energy:
        lowest_energy = energy
        best_energy_variant = variation

    if balance_score > best_balance_score:
        best_balance_score = balance_score
        best_balance_variant = variation

# Print results
print("Best performance (IPC):", best_ipc)
print(ET.tostring(best_ipc_variant, encoding='unicode'))

print("\nLowest energy:", lowest_energy)
print(ET.tostring(best_energy_variant, encoding='unicode'))

print("\nBest balance (IPC / energy*area):", best_balance_score)
print(ET.tostring(best_balance_variant, encoding='unicode'))
