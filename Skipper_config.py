# Configuration file

# Adjust REPO_PATH if necessary to make sure it contains the path to the pulled skipper repository when starting a skipper run
REPO_PATH = "/burg/mjlab/users/dsg2157/skipper"

########################################
# Customizable input files

MANIFEST = REPO_PATH + "/example/Example_manifest.csv"
# Repeat table
REPEAT_TABLE = REPO_PATH + "/annotations/repeatmasker.grch38.tsv.gz"
# Genome fasta
GENOME = "/burg/mjlab/projects/spidr-alignment-indices/GRCh38/GRCh38.primary_assembly.genome.fa"
# STAR reference
STAR_DIR = "/burg/mjlab/projects/spidr-alignment-indices/GRCh38/star"
# Generated from STAR index
CHROM_SIZES = STAR_DIR + "/chrNameLength.txt"
# Use a GFF filtered for genes expressed in the cell type of interest
GFF = REPO_PATH + "/annotations/gencode.v38.annotation.k562_totalrna.gt1.gff3.gz"
# Customizable, with defaults
# set to None for no blacklisting
BLACKLIST = REPO_PATH + "/annotations/encode3_eclip_blacklist.bed"
GENE_SETS = REPO_PATH + "/annotations/c5.go.v7.5.1.symbols.gmt"
GENE_SET_REFERENCE = REPO_PATH + "/annotations/encode3_go_terms.reference.tsv.gz"
GENE_SET_DISTANCE = REPO_PATH + "/annotations/encode3_go_terms.jaccard_index.rds"
# Ranked list of gene and transcript types found in GFF annotations
ACCESSION_RANKINGS = REPO_PATH + "/annotations/accession_type_ranking.txt"

########################################
# Customizable parameters

# Information about CLIP library
UMI_SIZE = 10
# Single-end: enter 1. Paired-end: enter read (1 or 2) corresponding to crosslink site
INFORMATIVE_READ = 1
# Internal use
UNINFORMATIVE_READ = 3 - INFORMATIVE_READ
# Use multiple input replicates to estimate overdispersion (preferred), or use multiple CLIP replicates
# Skipper requires replicates to model the variance in read counts.
OVERDISPERSION_MODE = "input"  # input or clip

########################################
# Intermediate files and scripts for the Skipper run, user setup not required. Adjust the paths if necessary.

# Skipper will partition the transcriptome and create feature annotations from the GFF
PARTITION = REPO_PATH + \
    "/annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.bed.gz"
FEATURE_ANNOTATIONS = REPO_PATH + \
    "/annotations/gencode.v38.annotation.k562_totalrna.gt1.tiled_partition.features.tsv.gz"
# Skipper will sort the repeat table.
REPEAT_BED = REPO_PATH + "/annotations/repeatmasker.grch38.sort.unique.bed.gz"
# The directory contains Skipper scripts
TOOL_DIR = REPO_PATH + "/tools"
