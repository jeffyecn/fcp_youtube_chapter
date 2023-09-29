import dataclasses

import fcp_youtube_chapter.timestamp


@dataclasses.dataclass
class Marker:
    name: str
    timestamp: int


def get_all_markers(fcp_element, start_seconds=0):
    element_start = fcp_youtube_chapter.timestamp.get_start_timestamp(fcp_element)
    element_offset = fcp_youtube_chapter.timestamp.get_offset_timestamp(fcp_element)

    if 'marker' == fcp_element.tag:
        yield Marker(fcp_element.attrib['value'], start_seconds + element_start)
    else:
        for child_element in fcp_element:
            yield from get_all_markers(child_element, start_seconds + element_offset - element_start)
