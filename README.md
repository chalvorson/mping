# mping
Colorful ping utility using Rich.

I needed an excuse to use Rich, so I built this simple multi-ping utility.  The ping metrics for one or more IPs are displayed in a Live Rich Table.

## Usage
To ping CloudFlare, Google, and Quad9 DNS servers 60 times...
> python mping.py -c 60 1.1.1.1 8.8.8.8 9.9.9.9

To ping until interrupted (ie. Ctrl-C), use -c 0
> python mping.py -c 0 192.168.1.1 1.1.1.1

The app depends on three main libraries.
- [Rich](https://rich.readthedocs.io/en/latest/) ([PyPI](https://pypi.org/project/rich/)) 
- [Pythonping](https://github.com/alessandromaggio/pythonping) ([PyPI](https://pypi.org/project/pythonping/))
- [Click](https://palletsprojects.com/p/click/) ([PyPI](https://pypi.org/project/click/))
