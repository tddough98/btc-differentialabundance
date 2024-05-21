import csv

from cirro.helpers.preprocess_dataset import PreprocessDataset

def make_samplesheet(ds):
    # Make a wide-form samplesheet with columns: sample, fastq_1, and fastq_2
    samplesheet = ds.wide_samplesheet()

    # Merge in the metadata for these samples (if any exists)
    samplesheet = pd.merge(samplesheet, ds.samplesheet, left_on="sample", right_on="sample")
    variable = ds.params["variable"]
    if variable not in samplesheet:
        raise ValueError(f"Column {variable} not found in samplesheet")

    # Save to a file
    samplesheet.to_csv("samplesheet.csv", index=None)

    # Set up a workflow param pointing to that file (e.g., for nf-core/rnaseq)
    ds.add_param("input", "samplesheet.csv")
    ds.logger.info(samplesheet.to_csv(index=None))

def make_contrasts(ds):
    # Generate the contrasts.csv
    reference = ds.params["reference"]
    target = ds.params["target"]
    ds.remove_param("reference")
    ds.remove_param("target")
    ds.remove_param("variable")

    with open("contrasts.csv", "w") as f:
        csv.writer(f).writerow(["id", "variable", "reference", "target"])
        csv.writer(f).writerow([f"{reference}_vs_{target}", variable, reference, target])
    with open("contrasts.csv", "r") as f:
        ds.logger.info(f.readlines())

if __name__ == "__main__":
    ds = PreprocessDataset.from_running()
    make_samplesheet(ds)
    make_contrasts(ds)
