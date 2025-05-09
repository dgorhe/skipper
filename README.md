# skipper
![Skipper cartoon](documents/logo.png)

Skip the peaks and expose RNA-binding in CLIP data

See published article in Cell Genomics: https://www.cell.com/cell-genomics/fulltext/S2666-979X(23)00085-X

<h2>Prerequisites</h2>
Skipper requires several executables and packages:

| Tool      | Link |
| ----------- | ----------- |
| R           | https://www.r-project.org/       |
| Python   | https://www.python.org/downloads/        |
| Conda/Mamba   | https://conda.io/projects/conda/en/latest/user-guide/install/index.html        |
| Snakemake   | https://snakemake.readthedocs.io/en/stable/getting_started/installation.html        |
| UMICollapse   | https://github.com/Daniel-Liu-c0deb0t/UMICollapse        |
| Skewer   | https://github.com/relipmoc/skewer        |
| Fastp    | https://github.com/OpenGene/fastp        |
| bedtools     | https://github.com/arq5x/bedtools2        |
| STAR   | https://github.com/alexdobin/STAR        |
| Java   | https://jdk.java.net/20/        |
| samtools | http://www.htslib.org/download/        |
| FastQC | https://www.bioinformatics.babraham.ac.uk/projects/fastqc/ |
| HOMER | http://homer.ucsd.edu/homer/introduction/install.html |

For example, below are some commands for installing Miniconda.

`curl -L -O "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"`

`bash Miniconda3-latest-Linux-x86_64.sh`

Skipper requires several python and R packages. In order to install the precise versions used in the manuscript, we have provided skipper_env.yaml to install the used versions of R and corresponding packages from source.

<h3>Option 1: Manual installation (Linux-amd64)</h3>

Use conda to create a snakemake environment for installing required packages:

`conda env create -f installation/skipper_env.yaml`

Use the install_umicollapse.sh script to complete installation of UMICollapse v1.0.0 in the installation folder. Expect the whole process to take around 30 seconds. 

`cd installation && ./install_umicollapse.sh`

Alternatively, at least as of this writing, Skipper is compatible with the newest version of R and its packages. The required R packages can be installed for an existing R installation as follows:

`install.packages(c("tidyverse", "VGAM", "viridis", "ggrepel", "RColorBrewer", "Rtsne", "ggupset", "ggdendro", "cowplot"))`

`if (!require("BiocManager", quietly = TRUE))`
    `install.packages("BiocManager")`
`BiocManager::install(c("GenomicRanges","fgsea","rtracklayer"))`

Paths to locally installed versions can be supplied in the config file, described below.

<h3>Option 2: Singularity installation (Linux-amd64)</h3>

`conda create -n snakemake snakemake==7.32.3 star==2.7.10b`

Singularity setup: https://docs.sylabs.io/guides/3.11/admin-guide/installation.html

<h2>Preparing to run Skipper</h2>
Skipper uses a Snakemake workflow. The `Skipper.py` file contains the rules necessary to process CLIP data from fastqs. Skipper also supports running on BAMs - note that Skipper's analysis of repetitive elements will assume that non-uniquely mapping reads are contained within the BAM files.

Providing an absolute path to the GitHub repository `REPO_PATH` will help Snakemake find resources regardless of the directory where Skipper is run.

Internal to the Yeo lab, setting the `REPO_PATH` to `/projects/ps-yeolab3/eboyle/encode/pipeline/github/yeo` will save time on preprocessing annotation files (check the annotation folder for HepG2, K562, or HEK293T. More annotations are available at `/projects/ps-yeolab4/software/skipper/1.0.0/bin/skipper/annotations/`).

Numerous resources must be entered in the `Skipper_config.py` file:

| Resource      | Description |
| ----------- | ----------- |
| MANIFEST            | Information on samples to run                                                        |
| GENOME              | Samtools- and STAR-indexed fasta of genome for the sample of interest                |
| STAR_DIR            | Path to STAR reference for aligning sequencing reads                |


Other paths to help Skipper run must be entered: 

| Path    | Description |
| ----------- | ----------- |
| EXE_DIR     | For convenience to point to stable locally installed software: it is added to PATH when Skipper runs |
| TOOL_DIR    | Directory for the tools located in the GitHub        |


Information about the CLIP library to be analyzed is also required:

| Setting      | Description |
| ----------- | ----------- |
| UMI_SIZE            | Bases to trim for deduplication (10 for current eCLIP)       |
| INFORMATIVE_READ    | Which read (1 or 2) reflects the crosslink site (for Paired End runs)        |
| OVERDISPERSION_MODE | Overdispersion can be estimated from multiple input replicates ("input") or multiple CLIP replicates ("clip"): "input" is recommended |


<h2>Customizable input for Skipper</h2>
Skipper accepts customizable files for several steps, which are also entered in the `Skipper_config.py` file: 

| Input      | Description |
| ----------- | ----------- |
| GFF                 | Gzipped gene annotation to partition the transcriptome and count reads.                       |
| PARTITION*           | Gzipped BED file of windows to test (can be generated from GFF file)                          |
| FEATURE_ANNOTATIONS* | Gzipped TSV file with the following columns: chrom,start,end,name,score,strand,feature_id,feature_bin,feature_type_top,feature_types,gene_name,gene_id, transcript_ids,gene_type_top,transcript_type_top,gene_types,transcript_types (can be generated from GFF file) |
| BLACKLIST           | Removes windows from reproducible enriched window files. Start and end coordinates must match tiled windows exactly.      |
| ACCESSION_RANKINGS  | A ranking of gene and transcript types present in the GFF to facilitate the transcriptome partitioning  |
| REPEAT_TABLE        | Coordinates of repetitive elements, available from UCSC Genome Browser               |
| REPEAT_BED*          | Gzipped sorted, nonoverlapping, tab-delimited annotations of repetitive elements: chr,start,end,label,score,strand,name,class,family,proportion_gc  |
| GENE_SETS           | GMT files of gene sets for gene set enrichment calculation |
| GENE_SET_REFERENCE  | TSV of gene set name, number of windows belonging to term, and fraction of windows that lie in gene set genes |
| GENE_SET_DISTANCE   | RDS of a matrix containing jaccard index scores for all pairs of gene sets in GMT file |

*Skipper can generate these files from other input, or you can make your own versions with the appropriate columns.

Want to make your own partition from RNA-seq of a sample? Run the tools/subset_gff.py script on RNA-seq quantifications from Salmon. We used a 1 TPM cutoff. Enter the resulting file for the GFF. This makes the window annotations more accurate but we haven’t carefully examined how important it is for the cell sample to match.

<h2>Making a manifest</h2>

| Column      | Description |
| ----------- | ----------- |
| Experiment       | CLIP samples will be compared against Input samples within an experiment. The same sample can be used in multiple experiments |
| Sample           | Each CLIP and Input sample will be processed separately until testing for differential binding   |
| Cells            | A place to record information on the cell sample used: this is not currently used in analysis  |
| Input_replicate  | Replicate # for the same Sample. The same Input replicate (fastq and number) can be used for multiple CLIP replicates |
| Input_adapter    | Fasta of adapter sequences for Input replicate                                                     |
| Input_fastq      | Path to Input replicate fastq (multiple files can be entered per cell to be concatenated            |
| Input_bam       | (Optional) Enter path to Input BAM file            |
| CLIP_replicate   | Replicate # for the same Sample. Distinct CLIP replicates are required |
| CLIP_adapter     | Fasta of adapter sequences for CLIP replicate                                                     |
| CLIP_fastq       | Path to CLIP replicate fastq (multiple files can be entered per cell to be concatenated            |
| CLIP_bam       | (Optional) Enter path to CLIP BAM file            |

Skipper requires multiple CLIP replicates of the same sample to call reproducible windows. Enter multiple replicates with the same experiment and sample columns on separate lines, incrementing the replicate number for each replicate. The same input replicate can be used in multiple experiments and repeated for the same sample if you estimate overdispersion from CLIP replicates. If the same replicate is used for multiple comparisons, the sample and replicate columns must be consistent.

See the example manifest in the example folder for the exact formatting and to test running Skipper by downloading the example dataset: https://zenodo.org/records/10636793.

<h2>Running Skipper</h2>

Skipper can be run like any other Snakemake workflow. 

Create a new directory to store output, copy the Snakemake and config files, and make all edits necessary to the config file. In the `all` rule of the `Skipper.py` file, comment out output that you do not wish to inspect.

Remember to load the Snakemake environment before running

`conda activate snakemake`

Use the dry run function to confirm that Snakemake can parse all the information:

`snakemake -ns Skipper.py -j 1`

Once Snakemake has confirmed DAG creation, if applicable, submit the jobs using high performance computing infrastructure options suit you:

<h3>Option 1: Manually installed packages</h3>

`snakemake -kps Skipper.py -w 15 -j 30`

`snakemake -kps Skipper.py -w 15 -j 30 --cluster "sbatch -t {params.run_time} -e {params.error_file} -o {params.out_file} -p condo -q condo -A csd792 --tasks-per-node {threads} --job-name {params.job_name} --mem {params.memory}"`

<h3>Option 2: Singularity</h3>

`snakemake -kps Skipper.py -w 15 -j 30 --use-singularity --singularity-args "--bind /tscc"`

`snakemake -kps Skipper.py -w 15 -j 30 --use-singularity --singularity-args "--bind /tscc" --cluster "sbatch -t {params.run_time} -e {params.error_file} -o {params.out_file} -p condo -q condo -A csd792 --tasks-per-node {threads} --job-name {params.job_name} --mem {params.memory}"`

Did Skipper terminate? Sometimes jobs fail - inspect any error output and rerun the same command if there is no apparent explanation such as uninstalled dependencies or a misformatted input file. Snakemake will try to pick up where it left off.

<h2>Skipper output</h2>

Skipper produces numerous output files. The `output/figures` directory contains figures summarizing the data.
| Output      | Description |
| ----------- | ----------- |
| all_reads       | Visualization of RNA region preferences based on total reads instead of called windows |
| threshold_scan  | Visualization of selection of minimum read coverage for statistical testing  |
| input_distributions | Visualization of betabinomial fits to aggregate data |
| enriched_windows | QC of called enriched windows  |
| enrichment_concordance  | Mosaic plot of agreement between called enriched windows between replicates |
| enrichment_reproducibility  | Number of total and enriched windows as a function of the number of replicates included  |
| reproducible_enriched_windows | Visualization of RNA region preferences for windows called by at least two replicates   |
| gene_sets        | Visualization of top enriched GO terms relative to ENCODE reproducible enriched windows   |
| clip_scatter_re  | Visualization of enriched repetitive elements   |
| tsne       | t-SNE visualization of binding preferences releative to ENCODE RBPs   |

Key outputs: Annotated reproducible enriched windows can be accessed at `output/reproducible_enriched_windows/` and Homer motif output is at `output/homer/`

Example CLIP fastqs and processed data are available at GEO and SRA: `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE213867`
