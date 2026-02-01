# consumptionCLI

![PyPI - Version](https://img.shields.io/pypi/v/consumptioncli) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/consumptioncli) ![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/t/track-44/consumptioncli) ![GitHub repo size](https://img.shields.io/github/repo-size/track-44/consumptioncli) ![PyPI - License](https://img.shields.io/pypi/l/consumptioncli) 

## About

Written in Python, **ConsumptionCLI** is a command line interface tool for keeping track of various forms of media. It acts as a simple alternative to online services such as *goodreads* and *bookmeter* for Novels or *IMDb* and *Letterboxd* for TV Shows and Movies. It also provides the flexibility to keep track of any number of other formats.

## Installation

### Method 1. pip install (Recommended)

#### Requirements

- Python 3.14+
- pip

#### Steps

1. Execute:
```sh
$ pip install consumptioncli
```

### Method 2. Self Build

#### Requirements

- Python 3+
- pip
- [PyPa's *build* frontend](https://github.com/pypa/build) 
- [consumptionbackend](https://github.com/t44dev/consumptionbackend)

#### Steps

> [!IMPORTANT]
> The same steps can and should be followed for **consumptionbackend** beforehand as **ConsumptionCLI** is dependent on it.

1. Clone the repository and navigate inside.
2. Execute:
```sh
$ python -m build
$ pip install .
```

## Basic Usage

**ConsumptionCLI** includes 3 primary entities:
- *Consumables* - Main entity type and are intended to represent Movies, TV Shows, Novels, etc.
- *Series* - Secondary entity. Each *Consumable* can be affiliated with one of these. Intended to represent an entire series, for example if a TV Show has multiple seasons each season may be represented with its own *Consumable* and all of these *Consumables* may be attached to the same *Series*.
- *Personnel* - Secondary entity. Can be affiliated with *Consumables* along with some role such as Author, Illustrator, Director, etc.

There are 5 main actions that can be performed on each of these entities: *New*, *Update*, *Delete*, *List*, and *View*. More details on these actions is given in the sections below.

### New

Concerned with the creation of entities. An example, demonstrating creating a *Consumable*, is given below:

{{PLACEHOLDER}}

On creation a view containing the values associated with the new entity is displayed. Each of these displayed fields can be adjusted manually using the appropriate options (e.g. `--rating NUMBER`). 

Some fields can be omitted and are filled with sensible defaults while others, such as `name` and `type` in the case of *Consumables*, are required.

Creation of *Series* and *Personnel* can be done with `series` and `personnel` in place of `consumable` respectively. 

Shorthand also exists for ease of use:

{{PLACEHOLDER}}

### Update

Concerned with changing fields of existing entities. Note that there are some constraints on how certain fields can be changed to maintain sensible states and consistency. 

A primary reason for making an update would be to change the status of a *Consumable*. There are 5 statuses that can be associated with any one *Consumable* including ```PLANNING```,```IN_PROGRESS```,```ON_HOLD```, ```DROPPED``` and ```COMPLETED```. By default *Consumables* are set in the ```PLANNING``` status. An example of updating a *Consumable* is given below:

{{PLACEHOLDER}}

Firstly, some search parameters are given which are used to find the desired entity(s). Then, the keyword `apply` is used indicate the following options are to specify changes. In the above example the status is set to ```IN_PROGRESS``` and the number of parts is set to 2; which could represent chapters read.

Note that if multiple *Consumables* match the search conditions then a confirmation prompt will be given. Additionally, fields such as names are not case-sensitive and only have to include part of the entire string allowing easy mass updating of related entities e.g. setting the same series for multiple *Consumables*. 

Dates are largely handled automatically, setting the status of a *Consumable* to ```IN_PROGRESS``` which does not have a start date will automatically set it to present day. 

> [!NOTE]
> If you want to update the date fields manually the default format is **YYYY/mm/dd** and so should be used when specifying a date using the ```--startdate``` and ```--enddate``` options. Alternatively, a different date format can be supplied using ```--dateformat```. E.g. ```--dateformat %d-%m-%Y```. See the [official specification](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for more details.

### Delete

Concerned with the deletion of entities. An example, demonstrating deleting a *Consumable*, is given below:

{{PLACEHOLDER}}

The same update search parameter logic applies to deletions. Again, confirmation of deletion will be required when multiple entities match the search parameters.

### List

Concerned with providing an overview of multiple entities can be viewed using the list action. The most basic usage is to provide no parameters and simply view all entities of a given type:

{{PLACEHOLDER}}

Listed entities have a default ordering, for example rating for *Consumables*, which can be changed using ```--order``` (and ```--reverse``` to reverse the order):

{{PLACEHOLDER}}

The entries can be filtered using search parameters:

{{PLACEHOLDER}}

### View

Concerned with viewing more details on a particular entity. This is most helpful for viewing relations between entities and tags on *Consumables*. An example, demonstrating viewing a *Consumable*, is given below:

{{PLACEHOLDER}}

### More

#### Help

The above overview outlines the fundamental use cases of **ConsumptionCLI**, however there are further complex possibilities. Specifically for *Consumables* there are many more actions that further streamline adding *Personnel*, assigning a *Series* and tagging. These possibilities and more can be explored using the ``--help`` flag after any given command or partial command.

```sh
$ cons --help
$ cons consumable new --help
```
