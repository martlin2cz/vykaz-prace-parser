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