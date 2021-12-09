In ADAM (the Climate database for Australia) [three times are stored for each observation](https://github.com/opencdms/opencdms-test-data/issues/10#issuecomment-667896059) - UTC, Local Time and Local Time ignoring daylight saving.

If the [Value Model](https://github.com/opencdms/opencdms-test-data/tree/e762ad087f38a6f4a1101c12adb5fe809018a93f/data_model_review#value-model) data model type was used, each of the three times would be repeated for each element (unless the schema split the time of the observation off from the value).
