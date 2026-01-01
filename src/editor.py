import defusedxml.ElementTree as ET

class Editor():
    """ Editor class """

    def _init__(self) -> None:
        self.namespace = self._get_namespaces(self.input_file)
        self.input_file = ET.parse(self.file)
        self.output_file = None

    def _get_namespaces(self, input_file) -> dict:
        """ Extract namesapces from a XML file """
        namespaces = {}
        for _, elem in ET.iterparse(input_file, events=('start-ns')):
            prefix, uri = elem
            namespaces[prefix] = uri
        return namespaces

    def edit_distance(tcx_file, distance) -> None:
        """ Edit distance in TCX file """
        pass
