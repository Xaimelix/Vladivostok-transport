from pathlib import Path
import copy
import xml.etree.ElementTree as ET

SRC = Path('Vladivostok-metro-map.svg')
DST = Path('transport-map.svg')

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

LINE_COLORS = {
    '#f24822': 'line-red',
    '#3dadff': 'line-blue',
    '#14ef10': 'line-green',
}

def attr(el, name):
    return el.attrib.get(name, '').lower()

def main():
    tree = ET.parse(SRC)
    root = tree.getroot()

    # Remove/replace only semantic attributes we add; keep Figma geometry intact.
    used = set()
    line_index = {name: 0 for name in LINE_COLORS.values()}
    station_index = 0

    # Main transport lines are the three stroked paths with stroke-width=4.
    for el in root.iter(f'{{{NS}}}path'):
        stroke = attr(el, 'stroke')
        if stroke in LINE_COLORS and attr(el, 'stroke-width') == '4':
            line_id = LINE_COLORS[stroke]
            idx = line_index[line_id]
            el.set('id', line_id if idx == 0 else f'{line_id}-{idx+1}')
            el.set('class', 'transport-line')
            line_index[line_id] += 1
            used.add(el.get('id'))

    # The exported map uses small colored rectangles AND filled paths as station ticks.
    for el in root.iter(f'{{{NS}}}path'):
        fill = attr(el, 'fill')
        if fill in LINE_COLORS and not attr(el, 'stroke'):
            station_index += 1
            el.set('id', f'station-marker-{station_index:02d}')
            el.set('class', 'station-marker')
            used.add(el.get('id'))

    for el in root.iter(f'{{{NS}}}rect'):
        fill = attr(el, 'fill')
        if fill in LINE_COLORS:
            station_index += 1
            el.set('id', f'station-marker-{station_index:02d}')
            el.set('class', 'station-marker')
            used.add(el.get('id'))

    # Circular nodes are the larger/interchange station markers.
    for el in root.iter(f'{{{NS}}}circle'):
        station_index += 1
        el.set('id', f'station-node-{station_index:02d}')
        el.set('class', 'station-node')
        used.add(el.get('id'))

    # Add a small stylesheet directly to the SVG. Existing appearance is preserved;
    # these classes only provide hooks for JS/CSS later.
    style = ET.Element(f'{{{NS}}}style')
    style.text = '''\n.transport-line { transition: opacity .25s ease, stroke-width .25s ease; }\n.station-marker, .station-node { transition: opacity .2s ease, transform .2s ease; transform-box: fill-box; transform-origin: center; }\n.transport-line.is-dimmed, .station-marker.is-dimmed, .station-node.is-dimmed { opacity: .22; }\n.transport-line.is-route { stroke-width: 7 !important; }\n.station-marker.is-route, .station-node.is-route { opacity: 1; }\n.station-node.is-origin, .station-node.is-destination { stroke-width: 4 !important; }\n'''
    root.insert(0, style)

    tree.write(DST, encoding='utf-8', xml_declaration=False)
    print(f'Created {DST}')
    print('Lines:')
    for k, v in line_index.items():
        print(f'  {k}: {v}')
    print(f'Station markers: {station_index}')

if __name__ == '__main__':
    main()
