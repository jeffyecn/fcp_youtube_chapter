import dataclasses


@dataclasses.dataclass
class Marker:
    name: str
    timestamp: float


class FcpXmlError(Exception):
    pass


def get_all_markers(fcp_root):
    last_marker_time = -1
    spine_element = get_spine_element_from_sequence(get_sequence_element(fcp_root))
    for element in spine_element:
        for marker in get_markers_from_clip_element(element):
            if marker.timestamp > last_marker_time:
                last_marker_time = marker.timestamp
                yield marker


def get_markers_from_clip_element(clip_element):
    for element in clip_element:
        if 'marker' == element.tag:
            marker_value = element.attrib['value']
            marker_timestamp = get_clip_start_time(clip_element) + get_timestamp(element.attrib['start'])
            yield Marker(marker_value, marker_timestamp)


def get_clip_start_time(clip_element):
    offset = get_timestamp(clip_element.attrib['offset'])
    return offset - get_timestamp(clip_element.attrib['start']) if 'start' in clip_element.attrib else offset


def get_library_element(fcp_root):
    for element in fcp_root:
        if 'library' == element.tag:
            return element
    raise FcpXmlError("No library element found")


def get_project_element_from_library(library_element):
    for element in library_element:
        if 'event' == element.tag:
            for event_child in element:
                if 'project' == event_child.tag:
                    return event_child
    raise FcpXmlError("No project element found")


def get_sequence_element_from_project(project_element):
    for element in project_element:
        if 'sequence' == element.tag:
            return element
    raise FcpXmlError("No sequence element found")


def get_sequence_element(fcp_root):
    library_element = get_library_element(fcp_root)
    project_element = get_project_element_from_library(library_element)
    sequence_element = get_sequence_element_from_project(project_element)
    return sequence_element


def get_spine_element_from_sequence(sequence_element):
    for element in sequence_element:
        if 'spine' == element.tag:
            return element
    raise FcpXmlError("No spine element found")


def get_project_duration(fcp_root):
    sequence_element = get_sequence_element(fcp_root)
    return get_timestamp(sequence_element.attrib['duration'])


def get_timestamp(timestamp_string):
    # convert timestamp string like 160/10s to seconds
    vals = [float(n) for n in timestamp_string.replace('s', '').split('/')]
    return vals[0] if 1 == len(vals) else vals[0] / vals[1]
