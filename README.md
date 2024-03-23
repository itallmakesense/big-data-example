# big-data-homework

### Solution
https://github.com/itallmakesense/big-data-homework/blob/main/SOLUTION.md

### Description

We are receiving data from external sources in the following structure:
```
{
  "DeviceId": "e35dea5d-615c-4ddb-a2ec-03124229bc0a",
  "Timestamp": 1502757714115,
  "Location": {
    "Country": "US",
    "City": "Port Huron",
    "Region": "Michigan",
    "ZipCode": 48060
  },
  "Packages": [
    {
      "Name": "package_1",
      "Version": "523.6672.123",
      "Type": "Internal",
      "Settings": [
        { "string.setting.name1": "value" },
        { "boolean.setting.name2": true },
        { "int.setting.name3": 251 }
      ]
    },
    {
      "Name": "package_2",
      "Version": "6.12",
      "Type": "External",
      "Settings": [
        { "string.setting.name1": "value" },
        { "boolean.setting.name2": true },
        { "int.setting.name3": 251 }
      ]
    }
  ]
}
```

- DeviceId - Unique device identifier. Count of devices is hundreds of millions.
- Timestamp - Timestamp when event has been received.
- Location - Device location information
- Packages - Package list installed on a device, can contain from 0 to few hundreds of packages:
  - Name - Package name
  - Version - Package version
  - Type - Package type (External or Internal)
  - Settings - Array of current settings values. Each package has unique list of settings (from 0 to few dozens)

These events are snapshots of packages installed on the device. Each active device sends this kind of events up to several times a day.
Geo distributed frontend servers receive events in real time in JSON format.

You need to design ETL process and data storage structure to be able to answer the following questions:
  - How many devices have installed specified packages by hours/days/weeks? Devices distribution
  by country/city/region. Please note that packages can be deleted from the device. When the
  package is deleted - it will not be present in the next snapshot.
  - How does the versions distribution for a particular package change over time?
  - How does the value distribution for a particular package setting change over time by package
  version?
  - Possibility to retrieve device list by value of a particular package setting at some point in time.

Following items are expected from you:
  - Select a technology for each key component of data processing system. Explain your choice.
  - Provide a high-level overview of the data flow architecture.
  - Show how the data is being loaded and transformed.
  - Provide the data processing algorithm written in any programming language (if applicable).
  - Describe the process of data visualization.
