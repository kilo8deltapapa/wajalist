# Generate Worked All Japan Prefectures List (from ADIF)

This program generates a list of Japan Prefectures that have been confirmed, a list of unconfirmed prefectures, and a mapchartSave.txt file for upload to https://www.mapchart.net/japan.html to visualize the prefectures.

## Requirements

- https://pypi.org/project/argparse/
- https://pypi.org/project/adif-io/

## Installation


## Usage

usage: wajalist.py [-h] [-c CALL [CALL ...]] [-b BAND] [-m MODE] [-s SAT] [--satonly] [--nosat] filename

positional arguments:
  filename

options:
 - -h, --help            show this help message and exit
 - -c CALL [CALL ...], --call CALL [CALL ...]
                        list of callsigns, if not specified all callsigns are considered
 - -b BAND, --band BAND  band (eg. 20M, 2M, 70CM, etc...), if not specified all bands are considered
 - -m MODE, --mode MODE  mode (eg. CW, SSB, FT8, etc...), if not specified all modes are considered
 - -s SAT, --sat SAT     satellite name (eg. RS-44, IO-117, etc...), if not specified all satellites are included
 - --satonly             include only satellite QSOs
 - --nosat               exclude satellite QSOs


## Related Projects


## Credits


## License

[MIT](LICENSE) © [kilo8deltapapa](https://github.com/kilo8deltapapa).
