import csv

from cirro.helpers.preprocess_dataset import PreprocessDataset


def make_samplesheet(ds):
    samplesheet = ds.samplesheet
    # Drop rows where sample column containing 'samtools'
    samplesheet = samplesheet[~samplesheet["sample"].str.contains("samtools")]

    variable = ds.params["variable"]
    if variable not in samplesheet:
        raise ValueError(f"Column {variable} not found in samplesheet")

    # Save to a file
    samplesheet.to_csv("samplesheet.csv", index=None)

    # Set up a workflow param pointing to that file (e.g., for nf-core/rnaseq)
    ds.logger.info(samplesheet.to_csv(index=None))


def make_contrasts(ds):
    # Generate the contrasts.csv
    variable = ds.params["variable"]
    reference = ds.params["reference"]
    target = ds.params["target"]
    ds.remove_param("reference")
    ds.remove_param("target")
    ds.remove_param("variable")

    with open("contrasts.csv", "w") as f:
        csv.writer(f).writerow(["id", "variable", "reference", "target"])
        csv.writer(f).writerow(
            [f"{reference}_vs_{target}", variable, reference, target]
        )
    with open("contrasts.csv", "r") as f:
        ds.logger.info(f.readlines())


if __name__ == "__main__":
    ds = PreprocessDataset.from_running()
    make_samplesheet(ds)
    make_contrasts(ds)
