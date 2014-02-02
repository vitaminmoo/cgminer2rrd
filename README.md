# cgminer2rrd

This repo is a set of helper scripts for pulling data out of the cgminer (or, preferably, sgminer) API and writing it to RRD files or a CSV. It's been developed on Linux, and may or may not work on other platforms.

## Requirements

* `python` 2.7
* `rrdtool-python`
* Optionally, `R` and `ggplot2`
* `sgminer` or `cgminer` - `sgminer` is preferable as it has more precision on the MHS API endpoint
* The API enabled for the above (add `"api-listen" : true,` to your cgminer config file)

## Usage

There are two primary usages of the scripts in this repo:

1. Recording long-term performance and tuning data to RRD files for later graphing
2. Actively fiddling with overclock settings while writing data to a CSV for later processing with `R`

## RRD Graphing

This is the, ironically, the less compelling usage of `cgminer2rrd` at the moment. It basically dumps information from the `cgminer` API to RRD files, ready for later graphing.

To run, use `./poll.py`, which will output very little, but poll the `cgminer` API every 5 seconds

To view data, use `./graph.py`, which will render the more useful generated RRD files to graphs, ready for viewing.

## Overclock Tuning

To generate a heatmap of your core/mem clock hashrate output:

1. Be aware of your card's stable range of core and memory clock settings
2. Customize the top of poll.py to specify these settings
3. Run `./poll.py` and wait several days
4. If `./poll.py` crashes or you have to stop it, just restart it when you can - it won't retry settings that it has already tried
5. Once `./poll.py` has finished, generate a graph with `R --no-save < clocks.R`
