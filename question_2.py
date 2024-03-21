import json
import tempfile

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    collect_set,
    countDistinct,
    explode,
    first,
    from_json,
    from_unixtime,
    get_json_object,
    map_keys,
    map_values,
    to_timestamp,
    window,
)
from pyspark.sql.types import ArrayType, MapType, StringType

spark = SparkSession.builder.getOrCreate()

df = (
    spark
    .readStream
    .format("kafka")
    # e.g. "devices_region_ny"
    .option("subscribePattern", "devices_region_.*")
    # We don't actually need to specify all the brokers,
    # even just one (but for the specific cluster) is enough
    .option("kafka.bootstrap.servers", "host1:port1,host2:port2,...")
    .load()
)

df = df.select(
    get_json_object(df.value, "$.DeviceId").alias("device_id"),
    get_json_object(df.value, "$.Timestamp").alias("timestamp"),
    explode(
        from_json(get_json_object(df.value, "$.Packages"), ArrayType(StringType()))
    ).alias("packages"),
)

df = df.withColumns(
        {
            "package_name": get_json_object("packages", "$.Name"),
            "package_version": get_json_object("packages", "$.Version"),
        }
    )
    .groupby("package_name", "package_version")
    .agg(
        first("timestamp").alias("timestamp")
    )  # first because events are always in ascending order
)

df.writeStream.partitionBy(
    "package_name",
    "timestamp",
).mode("overwrite").format(
    "parquet"
).save("s3a://big-data-homework/package_versions_over_time")
