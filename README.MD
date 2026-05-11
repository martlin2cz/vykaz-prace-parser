# vykaz-prace-parser

A tool which parses the work report from the proprietary text file format and exports in various other usefull formats.

# Input file format
The input file is a text file with the format like this:

```
23.04.2026 - DOLOREM (lorem) (7)
24.04.2026 - DOLOREM (lorem), LIPSUM (ipsum) (7 + 1)
```
While the hours can be unprecise, i.e.:
```
05.07.2026 - UNNUNEN (noon) (?)
05.07.2026 - BINUNEN (lesser), SECUNEN (morer), TERNEN (unoko) (3 + 5? + ?)
```
They can also be flagged "little more" or "little less":
```
12.10.2026 - NORNENER (non), LENENER (len), MORENER (moo) (2 + 3+ + 4-)
```
Or the hours can be ommited at all:
```
11.03.2026 - LOLOREM (nohours), BOLIPSUM (nohours too)
12.03.2026 - DONOMEM (nohours singular)
```


# Further features
If there are missing hours for some tasks, they will get automatically guessed (and vice versa):
```
07.09.2026 - MONON (qumun), YUNON (munon) (3)
08.09.2026 - VERYNON (yun) (2 + 4)
```
