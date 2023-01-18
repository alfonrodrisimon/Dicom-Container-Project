import os, sys

# Import libraries
from pydicom.charset import encode_string
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from datetime import datetime
from pydicom.uid import generate_uid

# Implement the handler for evt.EVT_C_FIND
def handle_find(event):

     """Handle a C-FIND request event."""
     ds = event.identifier

     # Get the query keys 
     # query = ( elem for elem in ds.iterall() if not elem.is_empty ) # generator expression

     # Generate response payload
     response = Dataset()

     

     #for elem in response.iterall():
      
      #response.clear(elem.tag)
     
     # for elem in query:
         # print(elem)

     # Create instances
     instances = []

     def build_mwl_entry():
        
        ds = Dataset()
        
        ds.SpecificCharacterSet = 'ISO_IR 100'
        ds.AccessionNumber = '09876543'
        ds.PatientName = 'MARÍA^LÓPEZ'
        ds.PatientID = '123456'
        ds.PatientBirthDate = '20000101'
        ds.PatientSex = 'M'
        ds.StudyInstanceUID = generate_uid()
        ds.RequestedProcedureDescription = 'Ophthalmic examination and evaluation'

        # Performed Procedure Step Relationship
        ds.ScheduledProcedureStepSequence = [Dataset()]
        step_seq = ds.ScheduledProcedureStepSequence
        step_seq[0].Modality = 'OP'
        step_seq[0].ScheduledStationAETitle = 'ARGOS'
        step_seq[0].ScheduledProcedureStepStartDate = datetime.now()
        step_seq[0].ScheduledProcedureStepStartTime= "0900"

        return ds

     response = build_mwl_entry()

     # Return all matches
     yield (0xFF00, response)

handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialise the Application Entity and specify the listen port
ae = AE()

# Add the supported presentation context
ae.add_supported_context(ModalityWorklistInformationFind)

# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)