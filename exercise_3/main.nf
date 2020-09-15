#!/usr/bin/env nextflow
params.input_dir = false
params.output_dir = false
params.fasta_pattern = false


if (params.input_dir) {
  input_dir = params.input_dir - ~/\/$/
  output_dir = params.output_dir - ~/\/$/
  fasta_pattern = params.fasta_pattern
  fasta_files = input_dir + '/' + fasta_pattern
  Channel
    .fromPath(fasta_files)
    .ifEmpty { error "Cannot find any fastas matching: ${fasta_files}" }
    .set { fastas }
}

//seqsero
process serotyping {
   memory '2 GB'
   publishDir "${output_dir}/seqsero",
   mode:'copy', 
   saveAs: { file -> "SeqSero_result_${fasta}_dir"}
 

  input:
  file (fasta) from fastas

  output:
  file('SeqSero_result_*') 

  """
  SeqSero2_package.py -m k -p 2 -t 4 -i ${fasta} 
  """
}
