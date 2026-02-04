This repository contains 
1.	Python script to generate a solved saved case file in PSSE 
2.	Python files to extract data from the Solved PSS(R)E saved case file using subsystem data retrieval APIs to save branch flows, area totals, generator data, bus voltages to Comma Separated File.
3.	.ipynb files to analyze the extracted csv files using Python Panda environment to filter branches and buses violating the specified limits.

Description of Files 
Generating saved case file:
1.	gen_change_ls.py is the automation script for generating the solved saved case file for each of the 7 different system topologies spanning 5 years including the present year when new resources solar, hydro, and wind were added to the system for 3 different load scenarios. 

Data extraction files 
The data extraction files are developed by taking brnflows_csv.py as a reference from PSSE's Example Folder. 
1. branch_loading.py – automation script to extract the loading data for all transformer and transmission line branches.
2. area_totals.py – automation script to extract area totals 
3. bus_voltage.py - automation script to extract bus voltage data
4. generation.py – automation script to extract generator data 

Data analysis files 
Analysis_Topology_0.ipynb – analysis of area totals, loading and voltage limit violations for Year 0, Topology 0

Area Total files 
These files are used to extract generation and load totals for each scenario by area,
contribution of each of the generators to considered load scenarios,
firm and non-firm capacity contributions of installed resources, and total load for the three scenarios for each of the studied topologies 
1.	Area_totals_Topology_1.ipynb – for Year 1, Topology 1
2.	Area_totals_Topology_2.ipynb – for Year 2, Topology 2
3.	Area_totals_Topology_3.ipynb – for Year 3, Topology 3
4.	Area_totals_Topology_4.ipynb – for Year 3, Topology 4
5.	Area_totals_Topology_5.ipynb – for Year 4, Topology 5
6.	Area_totals_Topology_6.ipynb – for Year 5, Topology 6

Limit checking files 
These files are used to extract loading values greater than 80% for transformer and transmission line branches, and bus voltages greater than 1.05 PU and less than 0.95 PU. 
1.	limit_checking_Topology_1.ipynb  - for Year 1, Topology 1
2.	limit_checking_Topology_2.ipynb - for Year 2, Topology 2
3.	limit_checking_Topology_3.ipynb- for Year 3, Topology 3
4.	limit_checking_Topology_4.ipynb- for Year 3, Topology 4
5.	limit_checking_Topology_5.ipynb- for Year 4, Topology 5
6.	limit_checking_Topology_6.ipynb- for Year 5, Topology 6


