def get_start_timestamp(fcp_element):
    return get_timestamp(fcp_element.attrib['start']) if 'start' in fcp_element.attrib else 0


def get_offset_timestamp(fcp_element):
    return get_timestamp(fcp_element.attrib['offset']) if 'offset' in fcp_element.attrib else 0


def get_timestamp(timestamp_string):
    # convert timestamp string like 160/10s to seconds
    vals = [float(n) for n in timestamp_string.replace('s', '').split('/')]
    return vals[0] if 1 == len(vals) else vals[0] / vals[1]
