# Description

An implementation of [rfc9402](https://datatracker.ietf.org/doc/html/rfc9402).

Supported notations (See Examples below):
- `<>`: grouping
- `/`: over
- `*`: multiple
- `+`: next
- `()`: round container
- `{}`: soft container
- `[]`: square container
- `@`: ball
- `cat`: cat

BNF:
```
concat    :  cat | ball | container | brace | paren | adjacent | multiple | over | group
group      :  "<" concat ">"
over      :  concat [ "/" concat ]
multiple  :  concat "*" /[0-9]+/
adjacent  :  concat [ "+" concat ]
paren     :  "(" [ concat ] ")"
brace     :  "{" [ concat ] "}"
container :  "[" [ concat ] "]"
ball      :  "@"
cat       :  "cat"
```

# Examples
```
$ ./concat.py 'cat'
 /\    /
(' )  (
 (  \  )
 |(__)/

$ ./concat.py [cat]
 --------
| /\    /|
|(' )  ( |
| (  \  )|
| |(__)/ |
 --------

$ ./concat.py 'cat + cat'
 /\    /  /\    /
(' )  (  (' )  (
 (  \  )  (  \  )
 |(__)/   |(__)/

$ ./concat.py 'cat / cat'
 /\    /
(' )  (
 (  \  )
 |(__)/
 /\    /
(' )  (
 (  \  )
 |(__)/

$ ./concat.py '<(cat * 2) + {@ + cat}> / [cat]'
  ~~~~~~~~~~~~~~~~~     -----------------
 ( /\    /  /\    /)   /          /\    /\
( (' )  (  (' )  (  ) /          (' )  (  |
(  (  \  )  (  \  ) ) |    __     (  \  ) |
 ( |(__)/   |(__)/ )   \ _/  \_@  |(__)/  |
  ~~~~~~~~~~~~~~~~~     \________________/
 --------
| /\    /|
|(' )  ( |
| (  \  )|
| |(__)/ |
 --------
```

# License
MIT