import argparse
import pathlib
from . import marker as fcp_youtube_chapter_marker
import sys
import xml.etree.ElementTree

def extract_chapters():
    parser = argparse.ArgumentParser(description='Extract chapters from Final Cut Pro XML file')
    parser.add_argument('fcp_xml_bundle', metavar='fcp_xml_bundle', type=str, nargs=1,
                        help='an FCP xml bundle to extract chapters from')
    args = parser.parse_args()
    fcp_xml_file = get_fcp_xml_file(args.fcp_xml_bundle[0])
    fcp_root = xml.etree.ElementTree.parse(fcp_xml_file).getroot()
    markers = fcp_youtube_chapter_marker.get_all_markers(fcp_root)
    print("=== Chapters ===")
    for marker in markers:
        print(f"{int(marker.timestamp/60):d}:{int(marker.timestamp)%60:02d} {marker.name}")


def get_fcp_xml_file(fcp_xml_bundle):
    bundle_path = pathlib.Path(fcp_xml_bundle)
    if bundle_path.suffix != '.fcpxmld':
        sys.exit("ERROR: fcp_xml_bundle must be a .fcpxmld bundle")
    if not bundle_path.is_dir():
        sys.exit("ERROR: fcp_xml_bundle must be a directory")
    fcp_xml_file = bundle_path / 'Info.fcpxml'
    if not fcp_xml_file.is_file():
        sys.exit("ERROR: fcp_xml_bundle must contain Info.fcpxml")
    return fcp_xml_file


if __name__ == "__main__":
    extract_chapters()
