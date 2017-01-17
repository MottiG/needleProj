__author__ = 'slouis'
# ERRONEOUS FILE : need to redo in PANDA data frames

import brewery
from brewery import ds
import sys
import os

os.chdir(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))

outputFilePath = os.path.join(os.getcwd(), 'data', 'interim','patentsMergedFields.txt')

sources = [
    {"file": os.path.join(os.getcwd(), 'data', 'raw','sample','patents.txt'),
     "fields": ["patentID","title","gdate"]},

    {"file": os.path.join(os.getcwd(), 'data', 'raw','sample','inventors.txt'),
     "fields": ["patentID","abstract"]},

    {"file": os.path.join(os.getcwd(), 'data', 'raw','sample','abstracts.txt'),
     "fields": ["patentID","firstname","lastname"]}
]

# Create list of all fields and add filename to store information
# about origin of data records
all_fields = brewery.FieldList(["file"])

# Go through source definitions and collect the fields
for source in sources:
    for field in source["fields"]:
        if field not in all_fields:
            all_fields.append(field)

out = ds.CSVDataTarget("patentsMergedFields.txt")
out.fields = brewery.FieldList(all_fields)
out.initialize()

for source in sources:
    path = source["file"]

    # Initialize data source: skip reading of headers - we are preparing them ourselves
    # use XLSDataSource for XLS files
    # We ignore the fields in the header, because we have set-up fields
    # previously. We need to skip the header row.

    src = ds.CSVDataSource(path,read_header=False,skip_rows=1)
    src.fields = ds.FieldList(source["fields"])
    src.initialize()

    for record in src.records():

        # Add file reference into ouput - to know where the row comes from
        record["file"] = path
        out.append(record)

    # Close the source stream
    src.finalize()
