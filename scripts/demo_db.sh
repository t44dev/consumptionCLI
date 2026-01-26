#!/usr/bin/env bash
set -Eeuo pipefail

export CONSUMPTION_CONFIG_DIR=.
export CONSUMPTION_DATA_DIR=.
export CONSUMPTION_LOG_DIR=.
C () {
    cons --force --dateformat "%Y-%m-%d%z" "$@"
}

if [ -f consumption.db ]; then
    rm consumption.db
    rm config.json
fi

# Consumables

## Novels - https://en.wikipedia.org/wiki/List_of_best-selling_books
C c n -t NOVEL -n "A Tale of Two Cities" -s PLANNING -mp 45 --tags yor1859,history
C c n -t NOVEL -n "Le Petit Prince" -s IN_PROGRESS -p 13 -mp 27 -sd "2000-01-02+0000" --tags yor1943,fable
C c n -t NOVEL -n "O Alquimista" -s COMPLETED -mp 5 -c 2 -r 8.9 -sd "2000-03-04+0000" -ed "2000-05-06+0000" --tags yor1988,allegorical
C c n -t NOVEL -n "The Hobbit" -s ON_HOLD -p 6 -mp 19 -sd "2000-07-08+0000" --tags yor1937,fantasy
C c n -t NOVEL -n "Dream of the Red Chamber" -s DROPPED -p 44 -mp 120 -r 3.4 -sd "2000-08-09+0000" -ed "2000-10-11+0000" --tags yor1791,romance

C c n -t NOVEL -n "Diary of a Wimpy Kid" -s COMPLETED -mp 217 -c 1 -r 5.2 -sd "2000-12-13+0000" -ed "2001-01-02+0000" --tags yor2007,comedy
C c n -t NOVEL -n "Rodrick Rules" -s ON_HOLD -p 144 -mp 217 -sd "2001-03-04+0000" --tags yor2008,comedy

C c n -t NOVEL -n "Welcome to Dead House" -s IN_PROGRESS -p 44 -mp 123 -sd "2001-07-08+0000" --tags yor1992,horror
C c n -t NOVEL -n "Stay Out of the Basement" -s PLANNING -mp 122 --tags yor1992,horror

C c n -t NOVEL -n "The Case of the Velvet Claws" -s DROPPED -p 144 -mp 215 -r 4.5 -sd "2001-09-10+0000" -ed "2001-11-12+0000" --tags yor1933,mystery

## Movies - https://en.wikipedia.org/wiki/List_of_highest-grossing_films
C c n -t MOVIE -n "A Tale of Two Cities" -s PLANNING -mp 1 --tags yor1958,history
C c n -t MOVIE -n "The Little Prince" -s COMPLETED -mp 1 -c 3 -r 7.6 -sd "2000-01-02+0000" -ed "2000-03-04+0000" --tags yor2015,fable
C c n -t MOVIE -n "The Hobbit: An Unexpected Journey" -s COMPLETED -mp 1 -c 1 -r 5.6 -sd "2000-05-06+0000" -ed "2000-07-08+0000" --tags yor2012,fantasy
C c n -t MOVIE -n "A Dream of Red Mansions" -s ON_HOLD -p 2 -mp 6 -sd "2000-09-10+0000" --tags yor1988,romance
C c n -t MOVIE -n "Diary of a Wimpy Kid" -s DROPPED -mp 1 -r 2.1 -sd "2000-11-12+0000" -ed "2001-01-02+0000" --tags yor2010,comedy

C c n -t MOVIE -n "Avatar" -s COMPLETED -mp 1 -c 1 -r 5.5 -sd "2001-03-04+0000" -ed "2001-05-06+0000" --tags yor2009,scifi
C c n -t MOVIE -n "Avatar: The Way of Water" -s PLANNING -mp 1 --tags yor2022,scifi

C c n -t MOVIE -n "Iron Man" -s COMPLETED -mp 1 -c 7 -r 6.2 -sd "2001-07-08+0000" -ed "2001-09-10+0000" --tags yor2008,scifi
C c n -t MOVIE -n "The Incredible Hulk" -s ON_HOLD -mp 1 -sd "2001-11-12+0000" --tags yor2008,scifi

C c n -t MOVIE -n "Titanic" -s DROPPED -mp 1 -r 2.0 -sd "2002-01-02+0000" -ed "2002-03-04+0000" --tags yor1997,romance,history

## TV Shows - https://www.imdb.com/search/title/?title_type=tv_series&sort=num_votes,desc
C c n -t TV -n "A Tale of Two Cities" -s PLANNING -mp 10 --tags yor1965,history
C c n -t TV -n "Dream of the Red Chamber" -s IN_PROGRESS -p 6 -mp 36 -sd "2000-01-02+0000" --tags yor1987,romance
C c n -t TV -n "Sherlock" -s COMPLETED -mp 15 -c 8 -r 7.9 -sd "2000-03-04+0000" -ed "2000-05-06+0000" --tags yor2010,mystery
C c n -t TV -n "Goosebumps: Season 1" -s ON_HOLD -p 8 -mp 10 -sd "2000-07-08+0000" --tags yor1995,horror
C c n -t TV -n "Perry Mason" -s DROPPED -p 244 -mp 271 -sd "2000-09-10+0000" -ed "2000-11-12+0000" --tags yor1957,mystery

C c n -t TV -n "Game of Thrones" -s PLANNING -mp 8 --tags yor2011,fantasy
C c n -t TV -n "Breaking Bad" -s IN_PROGRESS -p 3 -mp 5 -sd "2001-01-02+0000" --tags yor2008,crime
C c n -t TV -n "Stranger Things" -s COMPLETED -mp 5 -c 1 -r 4.4 -sd "2001-03-04+0000" -ed "2001-05-06+0000" --tags yor2016,drama
C c n -t TV -n "Friends" -s ON_HOLD -p 2 -mp 10 -sd "2001-07-08+0000" --tags yor1994,sitcom
C c n -t TV -n "The Walking Dead" -s DROPPED -p 1 -mp 11 -r 1.3 -sd "2001-09-10+0000" --tags yor2010,horror

# Series
C s n -n "A Tale of Two Cities"
C c s -n "A Tale of Two Cities" a -i 1

C s n -n "The Little Prince"
C c s -n "Prince" --tags fable a -i 2

C s n -n "Middle-Earth"
C c s -n "Hobbit" a -i 3

C s n -n "Dream of the Red Chamber"
C c s -n "Dream" a -i 4

C s n -n "Diary of a Wimpy Kid"
C c s -n "Wimpy" a -i 5
C c s -n "Rodrick" a -i 5

C s n -n "Goosebumps"
C c s -n "Goosebumps" a -i 6
C c s -n "Welcome to Dead House" a -i 6
C c s -n "Stay Out of the Basement" a -i 6

C s n -n "Perry Mason"
C c s -n "Perry Mason" a -i 7
C c s -n "Velvet Claws" a -i 7

C s n -n "Avatar"
C c s -n "Avatar" a -i 8

C s n -n "The Avengers"
C c s -n "Iron Man" a -i 9
C c s -n "Hulk" a -i 9

# Personnel
C p n -fn "Charles" -ln "Dickens"
C c p -t NOVEL -n "A Tale of Two Cities" a -i 1 -r Author

C p n -fn "Antoine" -ln "de Saint-Exupéry"
C c p -t NOVEL -n "Le Petit Prince" a -i 2 -r Author

C p n -fn "Paulo" -ln "Coelho"
C c p -t NOVEL -n "O Alquimista" a -i 3 -r Author

C p n -fn "John Ronald Reuel" -ln "Tolkien"
C c p -t NOVEL -n "Hobbit" a -i 4 -r Author

C p n -fn "Cao" -ln "Xueqin"
C c p -t NOVEL -n "Dream of the Red Chamber" a -i 5 -r Author

C p n -fn "Jeff" -ln "Kinney"
C c p -t NOVEL -n "Diary of a Wimpy Kid" a -i 6 -r Author,Illustrator
C c p -t NOVEL -n "Rodrick Rules" a -i 6 -r Author,Illustrator

C p n -fn "Robert Lawrence" -ln "Stine"
C c p -t NOVEL -n "Welcome to Dead House" a -i 7 -r Author
C c p -t NOVEL -n "Stay Out of the Basement" a -i 7 -r Author
C c p -t TV -n "Goosebumps" a -i 7 -r Creator

C p n -fn "Erle Stanley" -ln "Gardener"
C c p -t NOVEL -n "Velvet Claws" a -i 8 -r Author

C p n -fn "Erle Stanley" -ln "Gardener"
C c p -t NOVEL -n "Velvet Claws" a -i 9 -r Author

C p n -fn "Ralph" -ln "Thomas"
C c p -t MOVIE -n "A Tale of Two Cities" a -i 10 -r Director

C p n -fn "Mark" -ln "Osborne"
C c p -t MOVIE -n "Prince" a -i 11 -r Director

C p n -fn "Peter" -ln "Jackson"
C c p -t MOVIE -n "Hobbit" a -i 12 -r Director

C p n -fn "Xie" -ln "Tieli"
C p n -fn "Zhao" -ln "Yuan"
C c p -t MOVIE -n "Red Mansions" a -i 13 -r Director
C c p -t MOVIE -n "Red Mansions" a -i 14 -r Director

C p n -fn "Thor" -ln "Freudenthal"
C c p -t MOVIE -n "Diary of a Wimpy Kid" a -i 15 -r Director

C p n -fn "James" -ln "Cameron"
C c p -t MOVIE -n "Avatar" a -i 16 -r Director
C c p -t MOVIE -n "Titanic" a -i 16 -r Director

C p n -fn "Jon" -ln "Favreau"
C c p -t MOVIE -n "Iron Man" a -i 17 -r Director

C p n -fn "Louis" -ln "Leterrier"
C c p -t MOVIE -n "The Incredible Hulk" a -i 18 -r Director

C p n -fn "Joan" -ln "Craft"
C c p -t TV -n "A Tale of Two Cities" a -i 19 -r Director

C p n -fn "Wang" -ln "Fulin"
C c p -t TV -n "Dream of the Red Chamber" a -i 20 -r Director

C p n -fn "Mark" -ln "Gatiss"
C p n -fn "Steven" -ln "Moffat"
C c p -t TV -n "Sherlock" a -i 21 -r Creator
C c p -t TV -n "Sherlock" a -i 22 -r Creator

C p n -fn "Gail Patrick" -ln "Jackson"
C c p -t TV -n "Perry Mason" a -i 23 -r "Executive Producer"

C p n -fn "David" -ln "Benioff"
C p n -fn "Daniel Brett" -ln "Weiss"
C c p -t TV -n "Game of Thrones" a -i 24 -r "Creator"
C c p -t TV -n "Game of Thrones" a -i 25 -r "Creator"

C p n -fn "Vince" -ln "Gilligan"
C c p -t TV -n "Breaking Bad" a -i 26 -r "Creator"

C p n -fn "Matt" -ln "Duffer"
C p n -fn "Ross" -ln "Duffer"
C c p -t TV -n "Stranger Things" a -i 27 -r "Creator"
C c p -t TV -n "Stranger Things" a -i 28 -r "Creator"

C p n -fn "David" -ln "Crane"
C p n -fn "Marta" -ln "Kauffman"
C c p -t TV -n "Friends" a -i 29 -r "Creator"
C c p -t TV -n "Friends" a -i 30 -r "Creator"

C p n -fn "Frank" -ln "Darabont"
C c p -t TV -n "The Walking Dead" a -i 31 -r "Creator"

cons c l
cons s l
cons p l
