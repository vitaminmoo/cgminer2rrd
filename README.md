# cgminer2rrd

This repo is a set of helper scripts for pulling data out of the cgminer (or, preferably, sgminer) API and writing it to RRD files or a CSV. It's been developed on Linux, and may or may not work on other platforms.

## Requirements

* `python` 2.7
* `rrdtool-python`
* Optionally, `R`
* `sgminer` or `cgminer` - `sgminer` is preferable as it has more precision on the MHS API endpoint

## Usage

There are two primary usages of the scripts in this repo:

* Recording long-term performance and tuning data to RRD files for later graphing
* Actively fiddling with overclock settings while writing data to a CSV for later processing with `R`

## RRD Graphing


## Overclock Tuning
