# NOTE:
unfourtnly currently i cannot upload the complied vesion and the original dataset that has been used 
but you can complie it yourself using pyinstall, description are avialable 

corrently there is 3 scripts:
1) Id_to_bed
  * input1: CpGs id list
  * input2: length of extending sequence
    from each side of the CpG site
  * ouput: bed file for those CpGs sites.
    
3) graph_dis_by_id_with_GUI
  * input: methylation dataset and CpG list
  * output: plot for each CpG sites
    describing the distribution of beta-values across samples
    Y axis frequency, X axis beta-val range (0.0)
    
5) graph_by_cg_and_age_with_GUI
   * input: info dataset, methylation dataset, CpG list.
   * outut: plots for each CpG of the
     beta-value in Y axis and age in X axis



