#from ..src.data_model.dataset import Dataset
import pandas as pd
from io import BytesIO
from pathlib import Path
home = str(Path.home())

def dataset_definition():
    datasets = {}

    Dat1 = {"values":
                {'name': 'telva_dataset',
                 'target_index': ['date'],
                 'target_feature': 'water_flow',
                 'target_frequency': '1d',
                 'index_schema': '%Y-%m-%d',
                 'index_frequency': '10s'
                 },
            "files":
                {'dataset': open(home + "/aws/buckets/brain-iot/datasets/internal/EMALCSA_water_dam/1.Version_with_climate/telva_dataset.csv", "rb")}
            }

    # Dat2 = {'name': 'telva_dataset',
    #         'dataset': (BytesIO(b'my file contents'), "~/aws/buckets/brain-iot/datasets/internal/EMALCSA_water_dam/1.Version_with_climate/telva_dataset.csv"),
    #         'target_index': 'date',
    #         'target_feature': 'water_flow',
    #         'target_frequency': '1d',
    #         'index_schema': '%Y-%m-%d',
    #         'index_frequency': '10s'
    #        }
    # Dat2 = ed.ExtendedDataset(path="~/aws/buckets/brain-iot/datasets/internal/EMALCSA_consumption/1.Editable_version/Eiris/Eiris.csv",
    #                           index="Fecha", feature="Caudal", index_freq="20m", target_freq="1h", field_separator=";",
    #                           index_schema="%d/%m/%Y %H:%M:%S.%f")
    #
    # Dat3 = ed.ExtendedDataset(path="~/aws/buckets/brain-iot/datasets/external/AMPds/dataset.csv",
    #                           index="UNIX_TS", feature="UNE", index_freq="1h", target_freq="1d", field_separator=",")
    # Dat3.data.reset_index(inplace=True)
    # Dat3.data['UNIX_TS'] = pd.to_datetime(Dat3.data['UNIX_TS'], unit='s')
    # Dat3.data.set_index('UNIX_TS', inplace=True)

    datasets["all"] = [Dat1]
    # datasets["internal"] = [Dat1, Dat2]
    # datasets["external"] = [Dat3]
    # datasets["robotnik"] = []
    # datasets["emalcsa"] = [Dat1, Dat2]
    # datasets["resample_dataset"] = [Dat3]
    return datasets


def pytest_addoption(parser):
    parser.addoption("--datasets_s0nar", default="all", help="datasets can use the following options: all, internal, external, robotnik, emalcsa")


def pytest_generate_tests(metafunc):
    if "dataset" in metafunc.fixturenames:
        op = metafunc.config.getoption("datasets_s0nar")
        dataset_list = dataset_definition()[op]
        metafunc.parametrize("dataset", dataset_list)