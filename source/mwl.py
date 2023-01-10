# Import libraries
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from datetime import date

# Implement the handler for evt.EVT_C_FIND
def handle_find(event):

     """Handle a C-FIND request event."""
     ds = event.identifier

     # Create a MWL entry
     mwl = Dataset()

    # Add file meta information elements
     mwl.file_meta = FileMetaDataset()
     mwl.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
     mwl.file_meta.MediaStorageSOPClassUID = "1.2.276.0.7230010.3.1.0.1"
     mwl.file_meta.MediaStorageSOPInstanceUID = "1.2.276.0.7230010.3.1.4.2831176407.11154.1448031138.805061"
     mwl.file_meta.ImplementationClassUID = "1.2.276.0.7230010.3.0.3.6.0"
     mwl.file_meta.ImplementationVersionName = "OFFIS_DCMTK_360"

    # Add data elements
     #mwl.SpecificCharacterSet             = "ISO_IR 192"
     mwl.AccessionNumber                  = "123456789"
     mwl.PatientName                      = "SURNAME^NAME"
     mwl.PatientID                        = "987654321"
     mwl.OtherPatientIDs                  = "111111"
     mwl.PatientBirthDate                 = "19700101"
     mwl.PatientSex                       = "M"
     mwl.StudyInstanceUID                 = "1.2.276.0.75.2.1.11.1.1.1667387252720.80" 
     mwl.RequestedProcedureDescription    = "Ophthalmic examination and evaluation"
     mwl.ScheduledProcedureStepSequence   = [Dataset()]
     mwl.ScheduledProcedureStepSequence[0].Modality                           = "OP"
     mwl.ScheduledProcedureStepSequence[0].ScheduledStationAETitle            = "ARGOS"
     mwl.ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartDate    = "20230110"
     mwl.ScheduledProcedureStepSequence[0].ScheduledProcedureStepStartTime    = "080000"
     mwl.ScheduledProcedureStepSequence[0].ScheduledPerformingPhysicianName   = "Doctor"

     # Pending
     yield (0xFF00, mwl)

handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialise the Application Entity and specify the listen port
ae = AE()

# Add the supported presentation context
ae.add_supported_context(ModalityWorklistInformationFind)

# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)