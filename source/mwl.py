import os, sys

# Import libraries
from pydicom.dataset import Dataset, FileMetaDataset
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from datetime import datetime
from pydicom.uid import generate_uid,ExplicitVRLittleEndian

# Implement the handler for evt.EVT_C_FIND
def handle_find(event):

     """Handle a C-FIND request event."""
     ds = event.identifier

     # Function to DICOM Worklist entries
     def build_mwl_entry():
        
        ds = Dataset()
        
        # Add file meta information elements
        ds.file_meta = FileMetaDataset()
        ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        # Fill out the worklist query elements
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

     # Create instances
     instances = []
     mwl = build_mwl_entry()
     instances.append(mwl)

     matching = [inst for inst in instances if inst.ScheduledProcedureStepSequence[0].ScheduledStationAETitle == ds.ScheduledProcedureStepSequence[0].ScheduledStationAETitle] # generator expression

     for instance in matching: 
        
        # Return all matches
        yield (0xFF00, instance)

handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialise the Application Entity and specify the listen port
ae = AE()

# Add the supported presentation context
ae.add_supported_context(ModalityWorklistInformationFind)

# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)