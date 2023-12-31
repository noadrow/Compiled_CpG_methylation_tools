# NOTE:
Unfortunately, I cannot currently upload the compiled version and the original dataset that has been used. 
However, you can compile it yourself using PyInstaller. 
Detailed descriptions are available in the "installation_protocol.txt" file.
![Demo CountPages alpha](https://github.com/noadrow/Compiled_CpG_methylation_tools/blob/main/Gifs/pyinstaller.gif?raw=true)

1) Id_to_bed:
   - Input 1: CpGs ID list
   - Input 2: Length of extending sequence from each side of the CpG site
   - input 3: bed CpG reference file
   - Output: Bed file for those CpG sites.
   
## usage example converting horvarth CpG sites to a bed file
![Demo CountPages alpha](https://github.com/noadrow/Compiled_CpG_methylation_tools/blob/main/Gifs/ID_TO_%20BED.gif?raw=true)

2) graph_dis_by_id_with_GUI:
   - Input1: Methylation dataset
   - input2: CpG list
   - Output: A plot for each CpG site
     describing the distribution of
     beta-values across samples.
     The Y-axis represents frequency,
     The X-axis represents beta-value range (0.0).
   - counter: you can label the CpG sites for QC
## Example of plotting beta-distribution for group of CpG sites 
![Demo CountPages alpha](https://github.com/noadrow/Compiled_CpG_methylation_tools/blob/main/Gifs/DIS_PLOT.gif?raw=true)

3) graph_by_cg_and_age_with_GUI:
   - Input: Info dataset, methylation dataset, and CpG list
   - Output: Plots for each CpG:
     - The Y-axis represents the beta-values.
     - The X-axis represents chronological age.
     - Orange dots for women.
     - Blue dots for males.
     - json log config file for repeating runs
### manual configuration
![Demo CountPages alpha](https://github.com/noadrow/Compiled_CpG_methylation_tools/blob/main/Gifs/MHET_TO_AGE.gif?raw=true)

### using json log configuration
![Demo CountPages alpha](https://github.com/noadrow/Compiled_CpG_methylation_tools/blob/main/Gifs/METH_TO_AGE_json.gif?raw=true)

3) convert_to_pickle_with_gui:
   - Input1: A csv table you wish to convert
   - Input2: folder location to save the converted file 
   - Output: pickle file formated of the table 
