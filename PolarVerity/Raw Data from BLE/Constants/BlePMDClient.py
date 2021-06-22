from enum import Enum

class PMD_UUID(Enum):
    PMD_SERVICE = "FB005C80-02E7-F387-1CAD-8ACD2D8DF0C8"
    PMD_CP = "FB005C81-02E7-F387-1CAD-8ACD2D8DF0C8"
    PMD_DATA = "FB005C82-02E7-F387-1CAD-8ACD2D8DF0C8"

class PMD_MEASUREMENT_TYPE(Enum):
    ECG =0
    PPG =1
    ACC =2
    PPI =3
    BIOZ =4
    GYRO =5
    MAGNETOMETER =6
    BAROMETER =7
    AMBIENT =8
    SDK_MODE =9
    UNKNOWN_TYPE =255

class PMD_CP_RESPONSE_CODE(Enum):
    SUCCESS =0
    ERROR_INVALID_OP_CODE =1
    ERROR_INVALID_MEASUREMENT_TYPE =2
    ERROR_NOT_SUPPORTED =3
    ERROR_INVALID_LENGTH =4
    ERROR_INVALID_PARAMETER =5
    ERROR_ALREADY_IN_STATE =6
    ERROR_INVALID_RESOLUTION =7
    ERROR_INVALID_SAMPLE_RATE =8
    ERROR_INVALID_RANGE =9
    ERROR_INVALID_MTU =10
    ERROR_INVALID_NUMBER_OF_CHANNELS =11
    ERROR_INVALID_STATE =12
    ERROR_DEVICE_IN_CHARGER =13

class PMD_CP_COMMAND(Enum):
    NULL_ITEM =0
    GET_MEASUREMENT_SETTINGS =1
    REQUEST_MEASUREMENT_START =2
    STOP_MEASUREMENT =3
    GET_SDK_MODE_MEASUREMENT_SETTINGS =4

class PMD_SETTINGS(Enum):
    SAMPLE_RATE =0
    RESOLUTION =1
    RANGE =2
    RANGE_MILLIUNIT =3
    CHANNELS =4
    FACTOR =5

