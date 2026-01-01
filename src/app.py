import streamlit as st
import defusedxml.ElementTree as ET
import io

from editor import Editor

st.title("INBiT: A TCX-File Editor")
st.write("Upload your TCX file and type a distance")

uploaded_file = st.file_uploader("TCX file", type="xml")

if uploaded_file is not None:
    try:
        tree = ET.parse(uploaded_file)
        root = tree.getroot()

        # Edit part here
        # TBD

        # Security: Write the processed file to a memory buffer instead of to the hard disk
        buffer = io.BytesIO()
        tree.write(buffer, encoding='utf-8', xml_declaration=True)
        
        st.success("Processing complete!")

        st.download_button(
            label="Download edited TCX file",
            data=buffer.getvalue(),
            file_name=f"{uploaded_file}_edit.xml",
            mime="application/xml"
        )

    except Exception as e:
        st.error(f"Error: {e}")