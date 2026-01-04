import io
import re
from datetime import datetime

# XML packages
import xml.dom.minidom
import xml.etree.ElementTree as ET
import defusedxml.ElementTree as dET

class Editor():
    """ Editor class """

    def __init__(self, input_file) -> None:
        self.namespaces = self._get_namespaces(input_file)
        self._register_namespaces()
        self.input_file = dET.parse(input_file)
        self.output_file = None

    def _get_namespaces(self, input_file) -> dict:
        """ Extract namesapces from a XML file """
        namespaces = {}
        for _, elem in dET.iterparse(input_file, events=('start-ns', )):
            prefix, uri = elem

            if prefix == None:
                prefix = ''

            if prefix.startswith('ns') and re.match(r'ns\d+$', prefix):
                continue

            namespaces[prefix] = uri

        return namespaces
    
    def _register_namespaces(self) -> None:
        """ Registers the namespaces globally for ElementTree """
        for prefix, uri in self.namespaces.items():
            try:
                ET.register_namespace(prefix, uri)
            except ValueError as error:
                raise error

    # @classmethod
    def edit_distance(self, real_distance) -> None:
        """ Edit distance in TCX file """

        root = self.input_file.getroot()

        for activity in root.findall('.//Activity', self.namespaces):
            print(activity)
            for lap in activity.findall('Lap', self.namespaces):
                total_time_elem = lap.find('TotalTimeSeconds', self.namespaces)
                distance_elem = lap.find('DistanceMeters', self.namespaces)

                print(f'{lap} - {total_time_elem} - {distance_elem}')
                
                if total_time_elem is not None and distance_elem is not None:
                    total_seconds = float(total_time_elem.text)
                    distance_elem.text = str(real_distance)

                    print(f'{total_seconds} - {distance_elem.text}')
                    
                    start_time_str = lap.get('StartTime').replace('Z', '')
                    start_time = datetime.fromisoformat(start_time_str)

                    avg_pace = real_distance / total_seconds

                    print(f'AVG pace: {avg_pace}')

                    track = lap.find('Track', self.namespaces)
                    if track is not None:
                        for tp in track.findall('Trackpoint', self.namespaces):
                            time_elem = tp.find('Time', self.namespaces)
                            trackPoint_dist_elem = tp.find('DistanceMeters', self.namespaces)

                            print(f'{tp} - {time_elem} - {trackPoint_dist_elem}')
                            
                            if time_elem is not None and trackPoint_dist_elem is not None:
                                current_time_str = time_elem.text.replace('Z', '')
                                current_time = datetime.fromisoformat(current_time_str)
                                
                                elapsed = (current_time - start_time).total_seconds()
                                new_dist = elapsed * avg_pace

                                print(f'NEW distance: {new_dist}')
                                
                                # Ensure that the target is not overshoot (due to rounding)
                                if new_dist > real_distance:
                                    new_dist = real_distance
                                    
                                trackPoint_dist_elem.text = f"{new_dist:.2f}"
        buffer = io.BytesIO()
        self.input_file.write(buffer, encoding='utf-8', xml_declaration=True)
        
        self.output_file = buffer.getvalue()

if __name__ == "__main__":
    # Testing script
    print('Start testing...')
    print('Inint Editor')
    e = Editor("data/testfile.tcx")
    print('Editor initialized')
    print(f'Editor Namespaces: {e.namespaces}')
    new_distance = 30000
    print(f'Try to ad new distance: {new_distance}')
    e.edit_distance(30000)
    print(e.output_file)
    print('End testing!')