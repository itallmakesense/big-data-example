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
    get_json_object(df.value, "$.Location.Country").alias("country"),
    get_json_object(df.value, "$.Location.Region").alias("region"),
    get_json_object(df.value, "$.Location.City").alias("city"),
    explode(
        from_json(get_json_object(df.value, "$.Packages"), ArrayType(StringType()))
    ).alias("packages"),
).withColumns(
    {
        "timestamp": to_timestamp(from_unixtime("timestamp")),
        "package_name": get_json_object("packages", "$.Name"),
    }
)

devices_by_package_time_window = q1.groupby(
    "package_name",
    window("timestamp", "1 hour").alias("hour"),  # change for days and weeks windows accordingly
).agg(countDistinct("device_id").alias("devices_count"))

devices_by_location = q1.groupby("country", "region", "city").agg(
    countDistinct("device_id").alias("devices_count")
)

devices_by_package_time_window.writeStream.partitionBy(
    "package_name",
    "hour",  # or day or week, depending on the used time window
).mode("overwrite").format("parquet").save(
    "s3a://big-data-homework/devices_count_by_package_time_wondow"
)

devices_by_location.writeStream.partitionBy(
    "country",
    "region",
    "city",
).mode(
    "overwrite"
).format("parquet").save("s3a://big-data-homework/devices_count_by_location")
