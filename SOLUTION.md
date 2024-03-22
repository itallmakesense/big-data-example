### Assumptions
- `9 * 10^8` devices
- `200` countries
- `4000` regions
- `150000` cities
- `999` packages
- `999` package versions
- `999` package settings
- `9` package setting values
- `9` events per day
- `4000` geo distributed frontend servers (equal to the amount of regions)

### Conclusions
- `(9 * 10^8) / (4000) = 225000` devices per region
- `225000 * 9 = 2 * 10^6` devices events a day per region
- `4000` concurrent events readers (servers)
- How many devices have installed specified packages by hours/days/weeks?
  - `999 * (24 + 1 + 1/7) = 25118` writes per day, `9 * 10^6` writes per year
- Devices distribution by country/city/region:
  - `150000` (amount of cities) continuously updated records
- How does the versions distribution for a particular package change over time?
  - `(999 * 999 * 9) = 9 * 10^6` writes per day, `100` writes per second
- How does the value distribution for a particular package setting change over time by package version?
  - `(999 * 999 * 999 * 9 * 9) = 80 * 10^9` writes per day, `9 * 10^6` writes per second
- Possibility to retrieve device list by value of a particular package setting at some point in time:
  - `(999 * 999 * 9 * 9) = 80 * 10^6` writes per day, `1000` writes per second

### Technologies
- Apache Kafka for events production and consumption. It's a good pick to solve the problem of processing a large number of continuously emerging events, as it is a distributed event streaming tool, known for a high-performance, scalability, high availability, and at the same time not skipping durability property of the events data. Key things to figure out:
  - `2 * 10^6` devices events per day can be sent into one topic, so lets create dedicated topics for each region (`4000`), e.g. `devices_region_ny`
  - as we have assumed `4000` concurrent counsumers, which are not blocking each other, we would need the same amount of topic partitions. It's resulting in `16 * 10^6` partitions across all `4000` topics
  - having this big amount of partitions, we would need an adequate amount of processing power for them. Due to very little details, I'll assume that we would be ok with the amount of clusters equal to the number of countries (`200`), resulting in `80 * 10^3` partitions per cluster
  - As for the number of brokers, it's generally recommended to have less that `4000` partitions per broker, which gives us minimum of `20` brokers per cluster. Twice of that (`40`) will be a safer choise
- Apache Spark (PySpark) for events processing. It is scalable, funtional stream processing engine, that will allow to do all the required operations
- As it wasn't specified in what format specifically the results expected to be stored, as well as who will be using them or in what way they should be visualized, I'd pick a simple object storage, that should be distributed, partitionable and can be integrated with PySpark. For example, AWS S3
- As soon as data will be in object storage, it can be queried by many ways, starting from individually opening the result files, continuing with PySpark, and ending with tools like AWS Athena
