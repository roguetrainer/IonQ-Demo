import math

def generate_topology_svg(n_qubits=12):
    """
    Generates an SVG visualization of Linear vs All-to-All topologies.
    No matplotlib dependency.
    """

    width = 1400
    height = 600
    margin = 50

    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .title {{ font-size: 18px; font-weight: bold; text-anchor: middle; }}
            .node-label {{ font-size: 12px; font-weight: bold; text-anchor: middle; dominant-baseline: middle; fill: white; }}
            .edge-competitor {{ stroke: #999; stroke-width: 2; }}
            .edge-ionq {{ stroke: #4D96FF; stroke-width: 1; opacity: 0.2; }}
            .node-competitor {{ fill: #FF6B6B; stroke: #CC5555; stroke-width: 2; }}
            .node-ionq {{ fill: #4D96FF; stroke: #2565CC; stroke-width: 2; }}
        </style>
    </defs>

    <!-- Background -->
    <rect width="{width}" height="{height}" fill="white"/>

    <!-- LEFT: Competitor Linear Topology -->
    <g id="competitor">
        <!-- Title -->
        <text x="{width//4}" y="30" class="title">Competitor Architecture</text>
        <text x="{width//4}" y="55" class="title" font-size="14">(Nearest Neighbor Only)</text>

        <!-- Edges (linear chain) -->
'''

    # Compute positions for linear layout (left side)
    left_x_start = margin + 50
    left_x_end = width // 2 - margin - 50
    left_y = height // 2

    left_positions = []
    for i in range(n_qubits):
        x = left_x_start + (left_x_end - left_x_start) * i / (n_qubits - 1)
        left_positions.append((x, left_y))

    # Draw edges for linear
    for i in range(n_qubits - 1):
        x1, y1 = left_positions[i]
        x2, y2 = left_positions[i + 1]
        svg_content += f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge-competitor"/>\n'

    # Draw nodes for linear
    for i, (x, y) in enumerate(left_positions):
        svg_content += f'        <circle cx="{x}" cy="{y}" r="15" class="node-competitor"/>\n'
        svg_content += f'        <text x="{x}" y="{y}" class="node-label">{i}</text>\n'

    svg_content += '    </g>\n\n'

    # RIGHT: IonQ All-to-All Topology
    svg_content += '    <!-- RIGHT: IonQ All-to-All Topology -->\n    <g id="ionq">\n'

    # Title
    svg_content += f'        <text x="{3*width//4}" y="30" class="title">IonQ Architecture</text>\n'
    svg_content += f'        <text x="{3*width//4}" y="55" class="title" font-size="14">(All-to-All Connectivity)</text>\n'

    # Compute positions for circular layout (right side)
    center_x = width * 3 // 4
    center_y = height // 2
    radius = 100

    right_positions = []
    for i in range(n_qubits):
        angle = 2 * math.pi * i / n_qubits
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        right_positions.append((x, y))

    # Draw edges for all-to-all (in background)
    for i in range(n_qubits):
        for j in range(i + 1, n_qubits):
            x1, y1 = right_positions[i]
            x2, y2 = right_positions[j]
            svg_content += f'        <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="edge-ionq"/>\n'

    # Draw nodes for all-to-all
    for i, (x, y) in enumerate(right_positions):
        svg_content += f'        <circle cx="{x}" cy="{y}" r="12" class="node-ionq"/>\n'
        svg_content += f'        <text x="{x}" y="{y}" class="node-label" font-size="10">{i}</text>\n'

    svg_content += '    </g>\n'
    svg_content += '</svg>'

    # Write to file
    output_path = f"figures/topology_comparison_{n_qubits}qubits.svg"
    with open(output_path, 'w') as f:
        f.write(svg_content)

    print(f"✓ SVG visualization saved to: {output_path}")

if __name__ == "__main__":
    generate_topology_svg(n_qubits=12)
