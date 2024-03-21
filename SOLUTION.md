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
- Kafka for events production and consumption:
  - `2 * 10^6` devices events per day can be sent into one topic, so lets create dedicated topics for each region (`4000`), e.g. `devices_region_ny`
  - TBD
