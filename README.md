# GooglePlayCrawler

A python script to batch download mobile apps from Google Play Store. It supports batch downloading by collection/categorie (default to Top Free 120) as well as recording the information (such as downloads/version/size/ratings/supported Android version etc.) of downloaded APKs in a csv files.

## Getting Started

### Prerequisites

This project depends on a couple of unofficial Google Play APIs, and here is their installation instruction:

* [google-play-scraper](https://github.com/facundoolano/google-play-scraper) : Node.js module to scrape application data from the Google Play store.
```
npm install google-play-scraper
```
* [google-play-api](https://github.com/facundoolano/google-play-api) : Turns google-play-scraper into a RESTful API.
```
"download the repo using the link above"
cd {download folder}
npm install
```
* [gplaycli](https://github.com/matlink/gplaycli) : Google Play Downloader via Command line
```
pip3 install gplaycli
```

### Setup

Please make sure the config file for [gplaycli](https://github.com/matlink/gplaycli) is set correctly, and other prerequisites are working properly.

Change the GSCRAPPER_DIR in gpcconstants.py file to the folder where [google-play-api](https://github.com/facundoolano/google-play-api) is installed.

## Usage
```
python GooglePlayCrawler.py -d DIR (-a [ALL] -c [COLLECTION] -g [CATEGORY] -n [NUMBER] -s [START]
```

### Available Options
```
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     The folder to store the downloaded APKs (required)
  -a [ALL], --all [ALL]
                        Set this option to True will download all categories
                        (default: False)
  -c [COLLECTION], --collection [COLLECTION]
                        The collection to download from
                        {TOP_FREE,NEW_FREE,GROSSING,TRENDING} (default:
                        TOP_FREE)
  -g [CATEGORY], --category [CATEGORY]
                        The category to download (default: NONE; Available
                        options can be found in documentation).
  -n [NUMBER], --number [NUMBER]
                        The number of apps to download (default: 120; Max:
                        120).
  -s [START], --start [START]
                        The starting index of the retrieved list (default: 0;
                        Max: 500)
```

### Example

Check the available options:
```
python GooglePlayCrawler.py -h
```

Download the top 100 free apps from Google Play:
```
python GooglePlayCrawler.py -d DIR -n 100
```

Download the top 100 free apps from ANDROID_WEAR category:
```
python GooglePlayCrawler.py -d DIR -g ANDROID_WEAR -n 100
```

Download the top 50th to 100th new apps from SOCIAL category:
```
python GooglePlayCrawler.py -d DIR -g SOCIAL -n 50 -s 50
```

## Authors

* **Duling Lai** - *Single Contributor* - [DulingLai](https://github.com/DulingLai)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

