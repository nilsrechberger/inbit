import io
from datetime import datetime
import defusedxml.ElementTree as ET

class Editor():
    """ Editor class """

    def _init__(self, input_file) -> None:
        self.input_file = ET.parse(input_file)
        self.namespaces = self._get_namespaces(input_file)
        self.output_file = None

    def _get_namespaces(self, input_file) -> dict:
        """ Extract namesapces from a XML file """
        namespaces = {}
        for _, elem in ET.iterparse(input_file, events=('start-ns')):
            prefix, uri = elem
            namespaces[prefix] = uri
        return namespaces

    def edit_distance(self, real_distance) -> None:
        """ Edit distance in TCX file """
        root = self.input_file.getroot()

        for activity in root.findall('.//tcx:Activity', self.namespaces):
            for lap in activity.findall('tcx:Lap', self.namespaces):
                total_time_elem = lap.find('tcx:TotalTimeSeconds', self.namespaces)
                distance_elem = lap.find('tcx:DistanceMeters', self.namespaces)
                
                if total_time_elem is not None and distance_elem is not None:
                    total_seconds = float(total_time_elem.text)
                    distance_elem.text = str(real_distance)
                    
                    start_time_str = lap.get('StartTime').replace('Z', '')
                    start_time = datetime.fromisoformat(start_time_str)

                    avg_pace = real_distance / total_seconds

                    track = lap.find('tcx:Track', self.namespaces)
                    if track is not None:
                        for tp in track.findall('tcx:Trackpoint', self.namespaces):
                            time_elem = tp.find('tcx:Time', self.namespaces)
                            trackPoint_dist_elem = tp.find('tcx:DistanceMeters', self.namespaces)
                            
                            if time_elem is not None and trackPoint_dist_elem is not None:
                                current_time_str = time_elem.text.replace('Z', '')
                                current_time = datetime.fromisoformat(current_time_str)
                                
                                elapsed = (current_time - start_time).total_seconds()
                                new_dist = elapsed * avg_pace
                                
                                # Ensure that the target is not overshoot (due to rounding)
                                if new_dist > real_distance:
                                    new_dist = real_distance
                                    
                                trackPoint_dist_elem.text = f"{new_dist:.2f}"
        buffer = io.BytesIO()
        return self.input_file.write(buffer, encoding='utf-8', xml_declaration=True)


