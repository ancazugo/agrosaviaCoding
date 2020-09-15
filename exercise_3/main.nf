#!/usr/bin/env nextflow
params.input_dir = 'fastas'
params.output_dir = 'output'
params.fasta_pattern = '*.fasta'


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

//seqsero
process serotyping {
   memory '2 GB'
   publishDir "${output_dir}/sistr",
   mode:'copy', 
   saveAs: { file -> "Sistr_result_${fasta}_dir"}
 

  input:
  file (fasta) from fastas

  output:
  file('Sistr_result_*') 

  """
  sistr sistr --qc -vv --alleles-output ${fasta}_allele-results.json --novel-alleles ${fasta}_novel-alleles.fasta \
  --cgmlst-profiles ${fasta}_cgmlst-profiles.csv -f tab -o ${fasta}_sistr-output.tab ${fasta} 
  """
}