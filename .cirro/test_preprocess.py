import pytest

from cirro.helpers.preprocess_dataset import PreprocessDataset

from preprocess import make_contrasts, make_samplesheet


def test_preprocess():
    ds = PreprocessDataset(s3_dataset=".cirro/", config_directory="")
    make_samplesheet(ds)
    make_contrasts(ds)
