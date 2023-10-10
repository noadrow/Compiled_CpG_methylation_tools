# NOTE:
Unfortunately, I cannot currently upload the compiled version and the original dataset that has been used. 
However, you can compile it yourself using PyInstaller. 
Detailed descriptions are available in the "installation_protocol.txt" file.

Currently, there are three scripts:

1) Id_to_bed:
   - Input 1: CpGs ID list
   - Input 2: Length of extending sequence from each side of the CpG site
   - input 3: bed CpG reference file
   - Output: Bed file for those CpG sites.

2) graph_dis_by_id_with_GUI:
   - Input1: Methylation dataset
   - input2: CpG list
   - Output: A plot for each CpG site
     describing the distribution of
     beta-values across samples.
     The Y-axis represents frequency,
     The X-axis represents beta-value range (0.0).

3) graph_by_cg_and_age_with_GUI:
   - Input: Info dataset, methylation dataset, and CpG list
   - Output: Plots for each CpG:
     - The Y-axis represents the beta-values.
     - The X-axis represents chronological age.
     - Orange dots for women.
     - Blue dots for males.
