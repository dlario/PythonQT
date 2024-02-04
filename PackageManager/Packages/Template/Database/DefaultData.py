## Copyright 2023 David Lario
__author__ = 'David Lario'

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

## Revision History
## October 27, 2023 - David James Lario - Created

from PackageManager.Packages.ProgramBase.Database.dbProgramBase import *

def defaultData():
    defaultNameTextData = {"TableSelectionType": {"Table": TableSelectionType, "NameText": ["Single", "Multiple"]},
                           "DataType": {"Table": DataType,
                                        "NameText": ["Text", "Number", "Date", "Boolean", "Currency", "Percentage", "Time",
                                                 "Image",
                                                 "File"]},
                           "UnitType": {"Table": UnitType,
                                        "NameText": ["Length", "Area", "Volume", "Mass", "Time", "Speed", "Temperature",
                                                 "Energy",
                                                 "Power",
                                                 "Force", "Pressure", "Frequency", "Voltage", "Current", "Resistance",
                                                 "Capacitance",
                                                 "Inductance", "Charge", "Magnetic Flux", "Magnetic Flux Density",
                                                 "Illuminance",
                                                 "Luminous Flux", "Luminous Intensity", "Angle", "Solid Angle"]},
                           "Unit": {"Table": Unit, "NameText": ["Text", "Number", "Date", "Boolean", ]},
                           "LocationDescriptor": {"Table": LocationDescriptor,
                                                  "NameText": ["Text", "Number", "Date", "Boolean"]},
                           "ProgramName": {"Table": ProgramName,
                                           "NameText": ["Excel", "Word", "PowerPoint", "Outlook", "Access", "Publisher",
                                                    "OneNote"]},
                           "ProgramExtension": {"Table": ProgramExtension, "NameText": ["exe", "xls"]},
                           "Country": {"Table": Country, "NameText": ["Canada", "United States"]},
                           "City": {"Table": City, "NameText": ["Silver Valley", "Grande Prairie"]},
                           "AreaofGovernance": {"Table": AreaofGovernance, "NameText": []},
                           "MunicipalityType": {"Table": MunicipalityType,
                                                "NameText": ["Metropolitan", "District", "Local"]},
                           "Municipality": {"Table": Municipality, "NameText": []},
                           "First_Name": {"Table": First_Name, "NameText": ["David"]},
                           "FamilyName": {"Table": FamilyName, "NameText": ["Lario"]},
                           "ContactType": {"Table": ContactType,
                                           "NameText": ["Email", "Phone", "Fax", "Mobile", "Website", "Address"]},
                           "Gender": {"Table": Gender, "NameText": ["Male", "Female", "Other"]},
                           "Language": {"Table": Language, "NameText": ["English", "Mandarin Chinese", "Spanish",
                                                                              "Hindi", "Bengali",
                                                                              "Portuguese", "Russian", "Japanese",
                                                                              "Western Punjabi", "Marathi",
                                                                              "Telugu", "Wu Chinese", "Turkish",
                                                                              "Korean", "French", "German",
                                                                              "Vietnamese", "Tamil", "Yue Chinese",
                                                                              "Urdu", "Javanese", "Italian"]},
                           "NamePrefix": {"Table": NamePrefix, "NameText": ["Mr", "Mrs", "Ms", "Dr", "Prof"]},
                           "NameSuffix": {"Table": NameSuffix, "NameText": ["Jnr", "Snr", "III", "IV", "V"]},
                           "Profession": {"Table": Profession, "NameText": ["Engineer"]},
                           "ProfessionTag": {"Table": ProfessionTag, "NameText": []},
                           "ActivityPhase": {"Table": ActivityPhase,
                                             "NameText": ["Initiation", "Planning", "Execution",
                                                      "Monitoring and Controlling",
                                                      "Closing"]},
                           "BaseActivity": {"Table": BaseActivity, "NameText": ["Project", "Program", "Portfolio"]},
                           "TaskRelation": {"Table": TaskRelation,
                                            "NameText": ["Finish to Start", "Finish to Finish", "Start to Start",
                                                     "Start to Finish"]},
                           "TaskCategory": {"Table": TaskCategory, "NameText": []},
                           "TaskDescription": {"Table": TaskDescription, "NameText": []},
                           "TaskDetail": {"Table": TaskDetail, "NameText": []},
                           "JournalEntryType": {"Table": JournalEntryType,
                                                "NameText": ["Journal", "Event", "Corrective Action", "Defect",
                                                             "Communication"]},
                           "JournalEvent": {"Table": JournalEvent, "NameText": []},
                           "CorrectiveAction": {"Table": CorrectiveAction, "NameText": []},
                           "DefectSeverity": {"Table": DefectSeverity,
                                              "NameText": ["Critical", "High", "Medium", "Low"]},
                           "DefectCategory": {"Table": DefectCategory, "NameText": []},
                           "CommunicationType": {"Table": CommunicationType,
                                                 "NameText": ["Email", "Phone", "Fax", "Mobile", "Website", "Address"]},
                           "CompanyType": {"Table": CompanyType,
                                           "NameText": ["Client", "Supplier", "Sub-Contractor", "Consultant", "Employee",
                                                    "Other"]},
                           "JobTitle": {"Table": JobTitle, "NameText": []},
                           "Department": {"Table": Department, "NameText": ["Engineering", "Inspection"]},
                           "ActivityType": {"Table": ActivityType, "NameText": []},
                           "ActivityRole": {"Table": ActivityRole, "NameText": []},
                           "PaymentType": {"Table": PaymentType,
                                           "NameText": ["Cash", "Credit Card", "Debit Card", "Cheque", "EFT", "Other"]},
                           "PaymentStatus": {"Table": PaymentStatus, "NameText": ["Paid", "Unpaid", "Partially Paid"]},
                           "InventoryItem": {"Table": InventoryItem, "NameText": []},
                           "ContractTerms": {"Table": ContractTerms, "NameText": []},
                           "PhraseCategory": {"Table": PhraseCategory, "NameText": []},
                           "CompanyRelationshipType": {"Table": CompanyRelationshipType, "NameText": []},
                           "Status": {"Table": Status,
                                      "NameText": ["Active", "Inactive", "Pending", "Complete", "Cancelled"]},
                           "FilterType": {"Table": FilterType,
                                          "NameText": ["Text", "Number", "Date", "Boolean", "Currency", "Percentage",
                                                       "Time", "Image", "File"]},
                           "JournalItemRelationships": {"Table": JournalItemRelationships, "NameText": []},
                           "Award": {"Table": Award, "NameText": []}
                           }
    return defaultNameTextData
