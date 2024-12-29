# Serato Setlist Length Calculator

A Python script based on the Open-source work of the [Mixxx Contributers](https://github.com/mixxxdj/mixxx) for extracting Serato Metadata inside MP3s and FLAC files.

## Usage
``` shell
$ pip install -r requirements.txt
$ python3 combiner /path/to/_Serato_/Subcrates/your.crate
```
IMPORTANT: a specific pattern of cue points must be used within the Songs/Crate, without this the Script **WILL** result errors, or wrong values. This is defined lower within the README.

This will return a JSON Object in the following formating:
``` json
{
  "length": "13.12 minutes",
  "setlist": [
    [
      {
        "index": 0,
        "milliseconds": 1312
      },
      {
        "index": 1,
        "milliseconds": 161161
      },
      {
        "name": "Funny Song.mp3"
      }
    ],
    [
      {
        "index": 0,
        "milliseconds": 1337
      },
      {
        "index": 1,
        "milliseconds": 69696969
      },
      {
        "name": "Even funnier Song.flac"
      }
    ]
  ]
}
```
Here you can see 2 Cue Points per Song, the Song to which the Cue Points belong are specified in the `name` value. 

`Index` of cause describes the index of each Cue Point within the song.

The `milliseconds` value is the position of the cue point within the File, originating at 0ms (beginning of the song). This is fully independent of the beatgrid.

At the top of the Object is the `length` value, what we are ultimately after, that calcutes the approximate length of the Set in minutes (rounding to the 2nd decimal).

## specific pattern™

Within Serato you **MUST** use this following cue point pattern:

You will have to mark the start section and end ection of each track with 2 cue points, the start with the first (red) and the end with the second (orange).

The Cue2 of Song N must line up with Cue1 of Song N+1.
This should result in a continues strip of time that extends throughout the setlist.

The length of a Song is calculated by the following "formula":
`cue2.position - cue1.position`
This is repeated for every song in the Tracklist and should be sorted by index the same way it is within Serato. 

All the deltas are summed up and more or less we have the length of the set. This of cause will be inaccurate, this will ignore the beginning and end of the first/last song. (might be adressed in the future, or already is and i forgot to update the readme >.<)

## Credits
https://github.com/Holzhaus/serato-tags/blob/main/scripts/serato_markers2.py

https://gist.githubusercontent.com/kerrickstaley/8eb04988c02fa7c62e75c4c34c04cf02/raw/b7b37bed5df89f736d9bc3c865ea38e05d532668/parse_serato_crates.py

Without these 2 scripts this project would have been a major headache to realize within the 38C3, giant thanks.