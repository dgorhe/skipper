snakemake \
  -kps Skipper.smk \
  -w 15 \
  -j 50 \
  --rerun-incomplete \
  --cluster "sbatch -t {params.run_time} -e {params.error_file} -o {params.out_file} -p condo -q condo -A mjlab --tasks-per-node {threads} --job-name {params.job_name} --mem {params.memory}" \
  2>&1 | tee skipper.log
