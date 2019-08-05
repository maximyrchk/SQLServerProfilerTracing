#!/usr/bin/env python
# coding: utf-8

# #### Imports


import pandas as pd
import xml.etree.ElementTree as et
import lxml.etree as ET
import shutil as sh
import os


# #### Files
#  - XML_FILE : Tracing XML File from SQL Server Profiler
#  - XSLT_FORMAT : Format style file
#  - XML_TEMP : Temporary file that will be automatically created in process and will be deleted in the end
#  - OUT_FILE : result file that will be created automatically


XML_FILE = "test1.xml"
XSLT_FORMAT = "Format.xslt"
XML_TEMP = "TEMP.xml"
TXT_TEMP = "TEMP.txt"
OUT_FILE = "results.csv"


# #### Magic


# Changing first string to tracedata
temp = ET.parse(XML_FILE)
temp_str = ET.tostring(temp, pretty_print=True).decode()
with open(TXT_TEMP, "w") as f:
    f.write(temp_str)
from_file = open(TXT_TEMP) 
to_file = open(XML_TEMP, mode="w")
line = "<TraceData>"
to_file.write(line)
sh.copyfileobj(from_file, to_file)


# Converting XML using Format file
dom = ET.parse(XML_TEMP)
xslt = ET.parse(XSLT_FORMAT)
transform = ET.XSLT(xslt)
newdom = transform(dom)
a = ET.tostring(newdom, pretty_print=True).decode()
with open(XML_TEMP, "w") as f:
    f.write(a)



def parse_XML(xml_file, df_cols): 
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    out_df = pd.DataFrame(columns = df_cols)
    
    for node in xroot: 
        res = []
        for el in df_cols: 
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        out_df = out_df.append(pd.Series(res, index = df_cols), ignore_index=True)
        
    return out_df


# #### Change parameters if needed


# FOR FINDING INFO ABOUT CALCULATED COLUMNS
SEARCH_TEXT = "Finished processing calculated column"
# FOR EXTRACTING OTHER COLUMNS ADD THEM TO LIST
COLUMNS_LIST = ["Duration","TextData"]   


df = parse_XML(XML_TEMP, COLUMNS_LIST)
df = df[df["TextData"].str.contains(SEARCH_TEXT,na=False)]
df["Duration"] = df["Duration"].astype(int)
df["Duration In Minutes"] = (df["Duration"]/60000).round(2)
df.sort_values(by="Duration", ascending=False).to_csv(OUT_FILE, index=False)


# #### Deleting temp files


os.remove(XML_TEMP)
os.remove(TXT_TEMP)

