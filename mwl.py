# Import libraries
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian

from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind

# Implement the handler for evt.EVT_C_FIND
def handle_find(event):
     """Handle a C-FIND request event."""
     ds = event.identifier

     # Import stored SOP Instances
     instances = []

     ds1 = Dataset()

    # Add file meta information elements
     ds1.file_meta = FileMetaDataset()
     ds1.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
     ds1.file_meta.MediaStorageSOPClassUID = "0"
     ds1.file_meta.MediaStorageSOPInstanceUID = "0"

    # Fill out the worklist query elements
     ds1.SpecificCharacterSet             = "ISO_IR 6"
     ds1.InstanceCreationDate             = "20220101"
     ds1.AccessionNumber                  = "12345-abc"
     ds1.PatientName                      = "SURNAME^NAME"
     ds1.PatientID                        = "123456"
     ds1.PatientBirthDate                 = "19700101"
     ds1.PatientSex                       = "M"
     ds1.StudyInstanceUID                 = "1.45646.489451" 
     ds1.RequestedProcedureDescription    = "ProcedureDescription"
     ds1.ScheduledProcedureStepSequence   = [Dataset()]
     ds1.ScheduledProcedureStepSequence[0].Modality                           = "OT"
     ds1.ScheduledProcedureStepSequence[0].ScheduledStationAETitle            = "OT"
     ds1.ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartDate    = "20220101"
     ds1.ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartTime    = "080000"
     ds1.ScheduledProcedureStepSequence[0].ScheduledPerformingPhysicianName   = "Doctor Emmet Brown"
     ds1.ScheduledProcedureStepSequence[0].ScheduledProcedureStepDescription  = "SchedProcStepDesc"
     ds1.ScheduledProcedureStepID         = "0001"

     instances.append(ds1)

     if 'PatientName' in ds:
             if ds.PatientName not in ['*', '', '?']:
                 matching = [
                     inst for inst in instances if inst.PatientName == ds.PatientName
                 ]

     for instance in matching:

        # Check if C-CANCEL has been received
         if event.is_cancelled:
             yield (0xFE00, None)
             return
         
         identifier = Dataset()
         identifier.PatientName = instance.PatientName

         # Pending
         yield (0xFF00, identifier)

handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialise the Application Entity and specify the listen port
ae = AE()

# Add the supported presentation context
ae.add_supported_context(ModalityWorklistInformationFind)

# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)