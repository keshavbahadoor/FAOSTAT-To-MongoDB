# FAOSTAT To MongoDB

Simple, configurable, extendable data importer that imports FAO data into a mongodb instance. 

## Why is this needed?

FAOSTAT currently has an existing API. The current documentation, however, leaves much to be desired. I was never able to utilize the API to my requirements. The API mostly kept returning erroneous responses despite being correct as per the docs. 
This tool downloads the available bulk data dump from FAODATA (the URL is configurable) and then extracts, cleans and import data according to your specified configuration. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
Python 2.7.X 
pymongo
```

### Installing

Clone the repository as required 

```
git clone https://github.com/keshavbahadoor/FAOSTAT-To-MongoDB
```

Make sure you have pymongo installed 

```
pip install pymongo 
``` 

## Configuring what to import

The data_packages.json file contains a map configuration for available data zip files, and mongodb collections for importing int. This can be specified to your requirements.
 
```json 
[
  {
    "filename": "Trade_LiveAnimals_E_All_Data_(Normalized)",
    "collectionname": "livestock_all"
  },
  {
    "filename": "Prices_Monthly_E_All_Data_(Normalized)",
    "collectionname": "crop_price_monthly"
  }
]
```

## Importing Data 

Data is imported using the command line argument import_data

```
python faostat_to_mongodb import_data
```

After the import, all downloaded and extracted files are permanently deleted so as not to consume server space. 

## Logs
Logs are kept on a rotation basis and can be checked for cases where data is missing or corrupted. Instances of incorrect character encoding are usually cause for issues. 
Log rotation can be configured in config.py. 

## Contributing

Pull requests are welcomed :) 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

 

