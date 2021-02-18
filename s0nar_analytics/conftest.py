from data_models import extended_dataset as ed
import pandas as pd


def dataset_definition():
    datasets = {}
    Dat1 = ed.ExtendedDataset(
        path="~/aws/buckets/brain-iot/datasets/internal/EMALCSA_water_dam/1.Version_with_climate/telva_dataset.csv",
        index="date", feature="water_flow", index_freq="1d", target_freq="1d", index_schema="%Y-%m-%d")

    Dat2 = ed.ExtendedDataset(path="~/aws/buckets/brain-iot/datasets/internal/EMALCSA_consumption/1.Editable_version/Eiris/Eiris.csv",
                              index="Fecha", feature="Caudal", index_freq="20m", target_freq="1h", field_separator=";",
                              index_schema="%d/%m/%Y %H:%M:%S.%f")

    Dat3 = ed.ExtendedDataset(path="~/aws/buckets/brain-iot/datasets/external/AMPds/dataset.csv",
                              index="UNIX_TS", feature="UNE", index_freq="1h", target_freq="1d", field_separator=",")
    Dat3.data.reset_index(inplace=True)
    Dat3.data['UNIX_TS'] = pd.to_datetime(Dat3.data['UNIX_TS'], unit='s')
    Dat3.data.set_index('UNIX_TS', inplace=True)

    datasets["all"] = [Dat1, Dat1, Dat3]
    datasets["internal"] = [Dat1, Dat2]
    datasets["external"] = [Dat3]
    datasets["robotnik"] = []
    datasets["emalcsa"] = [Dat1, Dat2]
    datasets["resample_dataset"] = [Dat3]
    return datasets


def pytest_addoption(parser):
    parser.addoption("--datasets", default="all", help="datasets can use the following options: all, internal, external, robotnik, emalcsa")


def pytest_generate_tests(metafunc):
    if "dataset" in metafunc.fixturenames:
        op = metafunc.config.getoption("datasets")
        dataset_list = dataset_definition()[op]
        metafunc.parametrize("dataset", dataset_list)
    if "resample_dataset" in metafunc.fixturenames:
        dataset_list = dataset_definition()["resample_dataset"]
        metafunc.parametrize("resample_dataset", dataset_list)
    if "resample_threshold" in metafunc.fixturenames:
        metafunc.parametrize("resample_threshold", [0.2])
