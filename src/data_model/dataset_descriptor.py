from src import db


class DatasetDescriptor(db.EmbeddedDocument):
    """ The DatasetDescriptor class is an EmbeddedDocument of mongo. It aims to complete the definition of a document
    schema defined in the class Dataset. It declares several attributes needed to identify the main characteristics
    of the data. The required ones are target_index and target_feature.

    Attributes:
        index: A StringField indicating the variable used as index for the target feature. This field is required.
        target_feature: A StringField or a list of StringFields indicating the target features of the dataset. This field is required.
        target_frequency: A StringField indicating the desired frequency to achieved for the uses of the dataset
        index_unit: A StringField indicating the time unit of the index
        index_schema: A StringField or list of StringField indicating the fields were the data of the dataset is located
    """
    target_feature = db.StringField(required=True, regex='^(([a-zA-Z0-9]+)|([a-zA-Z0-9]+[_][a-zA-Z0-9]+))$')
    target_frequency = db.StringField(required=False, regex='^((([1-9]|[12][0-9]|3[01])[Dd])|(([1-9]|[1][0-9]|[2][0-3])[hH])|(([1-9]|[1-5][0-9])[mMsS]))$')
    index = db.StringField(required=True, regex='^(([a-zA-Z0-9]+)|([a-zA-Z0-9]+[_][a-zA-Z0-9]+))$')
    index_schema = db.StringField(required=False, regex='.*[%].+')
    index_frequency = db.StringField(required=False, regex='^((([1-9]|[12][0-9]|3[01])[Dd])|(([1-9]|[1][0-9]|[2][0-3])[hH])|(([1-9]|[1-5][0-9])[mMsS]))$')
    field_separator = db.StringField(required=False)


