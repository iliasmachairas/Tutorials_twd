# HEC_RAS_output_table

One of the deliverables in many hydrological studies for flood protection are hydraulic calculations which include various flow characteristics such as velocity, discharge, Froude number. HEC RAS is a popular software used in this kind of studies. One of its output is a .txt file which includes the data mentioned above. Importing it to excel, changing the style and its format, and exporting to pdf is a dull and time-conuming task. This is the problem I tried to solve. It is worth highlighting that the header (column names) has freezed and repeated in each page. <br />

The user just needs to upload the txt file and then they may select the outputs. There are three options:  <br />
(1) pdf document, <br />
(2) excel document, and <br />
(3) both of them. <br />
The default option is the second one. No software installation is required. <br />

To complete this task, Excel VBA and  a host of python libraries were used such as openpyxl, VBA, streamlit, and pandas.
