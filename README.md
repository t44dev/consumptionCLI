<!-- This README is generated and should not be edited directly. Instead edit the template at scripts/README_TEMPLATE.md -->
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

```sh
$ cons consumable new --name 1984 --type NOVEL
#31 [NOVEL] 1984
Series: None

0 Completions
PLANNING - 0/? Parts

No tags...
```

On creation a view containing the values associated with the new entity is displayed. Each of these displayed fields can be adjusted manually using the appropriate options (e.g. `--rating NUMBER`). 

Some fields can be omitted and are filled with sensible defaults while others, such as `name` and `type` in the case of *Consumables*, are required.

Creation of *Series* and *Personnel* can be done with `series` and `personnel` in place of `consumable` respectively. 

Shorthand also exists for ease of use:

```sh
$ cons c n -n "The Simpsons" -t TV
#32 [TV] The Simpsons
Series: None

0 Completions
PLANNING - 0/? Parts

No tags...
```

### Update

Concerned with changing fields of existing entities. Note that there are some constraints on how certain fields can be changed to maintain sensible states and consistency. 

A primary reason for making an update would be to change the status of a *Consumable*. There are 5 statuses that can be associated with any one *Consumable* including ```PLANNING```,```IN_PROGRESS```,```ON_HOLD```, ```DROPPED``` and ```COMPLETED```. By default *Consumables* are set in the ```PLANNING``` status. An example of updating a *Consumable* is given below:

```sh
$ cons consumable update --name 1984 apply --status IN_PROGRESS --parts 2
#    ID    Type    Series    Name    Parts    Rating      Completions  Status       Started     Completed
---  ----  ------  --------  ------  -------  --------  -------------  -----------  ----------  -----------
1    31    NOVEL   None      1984    2/?                            0  IN PROGRESS  2026/02/01
-    -     -       -         -       2/?                            0  -            -           -
1 Result...
```

Firstly, some search parameters are given which are used to find the desired entity(s). Then, the keyword `apply` is used indicate the following options are to specify changes. In the above example the status is set to ```IN_PROGRESS``` and the number of parts is set to 2; which could represent chapters read.

Note that if multiple *Consumables* match the search conditions then a confirmation prompt will be given. Additionally, fields such as names are not case-sensitive and only have to include part of the entire string allowing easy mass updating of related entities e.g. setting the same series for multiple *Consumables*. 

Dates are largely handled automatically, setting the status of a *Consumable* to ```IN_PROGRESS``` which does not have a start date will automatically set it to present day. 

> [!NOTE]
> If you want to update the date fields manually the default format is **YYYY/mm/dd** and so should be used when specifying a date using the ```--startdate``` and ```--enddate``` options. Alternatively, a different date format can be supplied using ```--dateformat```. E.g. ```--dateformat %d-%m-%Y```. See the [official specification](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) for more details.

### Delete

Concerned with the deletion of entities. An example, demonstrating deleting a *Consumable*, is given below:

```sh
$ cons consumable delete --name 1984
1 Consumable deleted.
```

The same update search parameter logic applies to deletions. Again, confirmation of deletion will be required when multiple entities match the search parameters.

### List

Concerned with providing an overview of multiple entities can be viewed using the list action. The most basic usage is to provide no parameters and simply view all entities of a given type:

```sh
$ cons consumable list
#    ID    Type    Series                Name                  Parts       Rating    Completions  Status       Started     Completed
---  ----  ------  --------------------  --------------------  --------  --------  -------------  -----------  ----------  -----------
1    1     NOVEL   A Tale of Two Cities  A Tale of Two Cities  0/45                            0  PLANNING
2    2     NOVEL   The Little Prince     Le Petit Prince       13/27                           0  IN PROGRESS  2000/01/02
3    4     NOVEL   Middle-Earth          The Hobbit            6/19                            0  ON HOLD      2000/07/08
4    7     NOVEL   Diary of a Wimpy Kid  Rodrick Rules         144/217                         0  ON HOLD      2001/03/04
5    8     NOVEL   Goosebumps            Welcome to Dead Hou.  44/123                          0  IN PROGRESS  2001/07/08
6    9     NOVEL   Goosebumps            Stay Out of the B...  0/122                           0  PLANNING
7    11    MOVIE   A Tale of Two Cities  A Tale of Two Cities  0/1                             0  PLANNING
8    14    MOVIE   Dream of the Red ...  A Dream of Red Ma...  2/6                             0  ON HOLD      2000/09/10
9    17    MOVIE   Avatar                Avatar: The Way o...  0/1                             0  PLANNING
10   19    MOVIE   The Avengers          The Incredible Hulk   0/1                             0  ON HOLD      2001/11/12
11   21    TV      A Tale of Two Cities  A Tale of Two Cities  0/10                            0  PLANNING
12   22    TV      Dream of the Red ...  Dream of the Red ...  6/36                            0  IN PROGRESS  2000/01/02
13   24    TV      Goosebumps            Goosebumps: Season 1  8/10                            0  ON HOLD      2000/07/08
14   25    TV      Perry Mason           Perry Mason           244/271                         0  DROPPED      2000/09/10  2000/11/12
15   26    TV      None                  Game of Thrones       0/8                             0  PLANNING
16   27    TV      None                  Breaking Bad          3/5                             0  IN PROGRESS  2001/01/02
17   29    TV      None                  Friends               2/10                            0  ON HOLD      2001/07/08
18   32    TV      None                  The Simpsons          0/?                             0  PLANNING
19   30    TV      None                  The Walking Dead      1/11          1.3               0  DROPPED      2001/09/10
20   20    MOVIE   None                  Titanic               0/1           2                 0  DROPPED      2002/01/02  2002/03/04
21   15    MOVIE   Diary of a Wimpy Kid  Diary of a Wimpy Kid  0/1           2.1               0  DROPPED      2000/11/12  2001/01/02
22   5     NOVEL   Dream of the Red ...  Dream of the Red ...  44/120        3.4               0  DROPPED      2000/08/09  2000/10/11
23   28    TV      None                  Stranger Things       5/5           4.4               1  COMPLETED    2001/03/04  2001/05/06
24   10    NOVEL   Perry Mason           The Case of the V...  144/215       4.5               0  DROPPED      2001/09/10  2001/11/12
25   6     NOVEL   Diary of a Wimpy Kid  Diary of a Wimpy Kid  217/217       5.2               1  COMPLETED    2000/12/13  2001/01/02
26   16    MOVIE   Avatar                Avatar                1/1           5.5               1  COMPLETED    2001/03/04  2001/05/06
27   13    MOVIE   Middle-Earth          The Hobbit: An Un...  1/1           5.6               1  COMPLETED    2000/05/06  2000/07/08
28   18    MOVIE   The Avengers          Iron Man              1/1           6.2               7  COMPLETED    2001/07/08  2001/09/10
29   12    MOVIE   The Little Prince     The Little Prince     1/1           7.6               3  COMPLETED    2000/01/02  2000/03/04
30   23    TV      None                  Sherlock              15/15         7.9               8  COMPLETED    2000/03/04  2000/05/06
31   3     NOVEL   None                  O Alquimista          5/5           8.9               2  COMPLETED    2000/03/04  2000/05/06
-    -     -       -                     -                     907/1506      4.97             24  -            -           -
31 Results...
```

Listed entities have a default ordering, for example rating for *Consumables*, which can be changed using ```--order``` (and ```--reverse``` to reverse the order):

```sh
$ cons consumable list --order name --reverse
#    ID    Type    Series                Name                  Parts       Rating    Completions  Status       Started     Completed
---  ----  ------  --------------------  --------------------  --------  --------  -------------  -----------  ----------  -----------
1    8     NOVEL   Goosebumps            Welcome to Dead Hou.  44/123                          0  IN PROGRESS  2001/07/08
2    20    MOVIE   None                  Titanic               0/1           2                 0  DROPPED      2002/01/02  2002/03/04
3    30    TV      None                  The Walking Dead      1/11          1.3               0  DROPPED      2001/09/10
4    32    TV      None                  The Simpsons          0/?                             0  PLANNING
5    12    MOVIE   The Little Prince     The Little Prince     1/1           7.6               3  COMPLETED    2000/01/02  2000/03/04
6    19    MOVIE   The Avengers          The Incredible Hulk   0/1                             0  ON HOLD      2001/11/12
7    13    MOVIE   Middle-Earth          The Hobbit: An Un...  1/1           5.6               1  COMPLETED    2000/05/06  2000/07/08
8    4     NOVEL   Middle-Earth          The Hobbit            6/19                            0  ON HOLD      2000/07/08
9    10    NOVEL   Perry Mason           The Case of the V...  144/215       4.5               0  DROPPED      2001/09/10  2001/11/12
10   28    TV      None                  Stranger Things       5/5           4.4               1  COMPLETED    2001/03/04  2001/05/06
11   9     NOVEL   Goosebumps            Stay Out of the B...  0/122                           0  PLANNING
12   23    TV      None                  Sherlock              15/15         7.9               8  COMPLETED    2000/03/04  2000/05/06
13   7     NOVEL   Diary of a Wimpy Kid  Rodrick Rules         144/217                         0  ON HOLD      2001/03/04
14   25    TV      Perry Mason           Perry Mason           244/271                         0  DROPPED      2000/09/10  2000/11/12
15   3     NOVEL   None                  O Alquimista          5/5           8.9               2  COMPLETED    2000/03/04  2000/05/06
16   2     NOVEL   The Little Prince     Le Petit Prince       13/27                           0  IN PROGRESS  2000/01/02
17   18    MOVIE   The Avengers          Iron Man              1/1           6.2               7  COMPLETED    2001/07/08  2001/09/10
18   24    TV      Goosebumps            Goosebumps: Season 1  8/10                            0  ON HOLD      2000/07/08
19   26    TV      None                  Game of Thrones       0/8                             0  PLANNING
20   29    TV      None                  Friends               2/10                            0  ON HOLD      2001/07/08
21   5     NOVEL   Dream of the Red ...  Dream of the Red ...  44/120        3.4               0  DROPPED      2000/08/09  2000/10/11
22   22    TV      Dream of the Red ...  Dream of the Red ...  6/36                            0  IN PROGRESS  2000/01/02
23   6     NOVEL   Diary of a Wimpy Kid  Diary of a Wimpy Kid  217/217       5.2               1  COMPLETED    2000/12/13  2001/01/02
24   15    MOVIE   Diary of a Wimpy Kid  Diary of a Wimpy Kid  0/1           2.1               0  DROPPED      2000/11/12  2001/01/02
25   27    TV      None                  Breaking Bad          3/5                             0  IN PROGRESS  2001/01/02
26   17    MOVIE   Avatar                Avatar: The Way o...  0/1                             0  PLANNING
27   16    MOVIE   Avatar                Avatar                1/1           5.5               1  COMPLETED    2001/03/04  2001/05/06
28   1     NOVEL   A Tale of Two Cities  A Tale of Two Cities  0/45                            0  PLANNING
29   11    MOVIE   A Tale of Two Cities  A Tale of Two Cities  0/1                             0  PLANNING
30   21    TV      A Tale of Two Cities  A Tale of Two Cities  0/10                            0  PLANNING
31   14    MOVIE   Dream of the Red ...  A Dream of Red Ma...  2/6                             0  ON HOLD      2000/09/10
-    -     -       -                     -                     907/1506      4.97             24  -            -           -
31 Results...
```

The entries can be filtered using search parameters:

```sh
$ cons consumable list --type NOVEL
#    ID    Type    Series                Name                  Parts       Rating    Completions  Status       Started     Completed
---  ----  ------  --------------------  --------------------  --------  --------  -------------  -----------  ----------  -----------
1    1     NOVEL   A Tale of Two Cities  A Tale of Two Cities  0/45                            0  PLANNING
2    2     NOVEL   The Little Prince     Le Petit Prince       13/27                           0  IN PROGRESS  2000/01/02
3    4     NOVEL   Middle-Earth          The Hobbit            6/19                            0  ON HOLD      2000/07/08
4    7     NOVEL   Diary of a Wimpy Kid  Rodrick Rules         144/217                         0  ON HOLD      2001/03/04
5    8     NOVEL   Goosebumps            Welcome to Dead Hou.  44/123                          0  IN PROGRESS  2001/07/08
6    9     NOVEL   Goosebumps            Stay Out of the B...  0/122                           0  PLANNING
7    5     NOVEL   Dream of the Red ...  Dream of the Red ...  44/120         3.4              0  DROPPED      2000/08/09  2000/10/11
8    10    NOVEL   Perry Mason           The Case of the V...  144/215        4.5              0  DROPPED      2001/09/10  2001/11/12
9    6     NOVEL   Diary of a Wimpy Kid  Diary of a Wimpy Kid  217/217        5.2              1  COMPLETED    2000/12/13  2001/01/02
10   3     NOVEL   None                  O Alquimista          5/5            8.9              2  COMPLETED    2000/03/04  2000/05/06
-    -     -       -                     -                     617/1110       5.5              3  -            -           -
10 Results...
```

### View

Concerned with viewing more details on a particular entity. This is most helpful for viewing relations between entities and tags on *Consumables*. An example, demonstrating viewing a *Consumable*, is given below:

```sh
$ cons consumable view --id 1
#1 [NOVEL] A Tale of Two Cities
Series: A Tale of Two Cities

0 Completions
PLANNING - 0/45 Parts

Tags: history, yor1859

Personnel:
#    ID    Name             Role
---  ----  ---------------  ------
1    1     Charles Dickens  Author
-    -
1 Result...
```

### More

#### Help

The above overview outlines the fundamental use cases of **ConsumptionCLI**, however there are further complex possibilities. Specifically for *Consumables* there are many more actions that further streamline adding *Personnel*, assigning a *Series* and tagging. These possibilities and more can be explored using the ``--help`` flag after any given command or partial command.

```sh
$ cons --help
$ cons consumable new --help
```
