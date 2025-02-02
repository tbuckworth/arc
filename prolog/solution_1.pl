
vertical_colour(C,Colour):-
    input_colour(R,C,Colour),
    R is 0,
    Colour \= black.

vertical_colour(C,Colour):-
    nrow(NR),
    R is NR - 1,
    input_colour(R,C,Colour),
    Colour \= black.

horizontal_colour(R,Colour):-
    input_colour(R,C,Colour),
    C is 0,
    Colour \= black.

horizontal_colour(R,Colour):-
    ncol(NC),
    C is NC-1,
    input_colour(R,C,Colour),
    Colour \= black.

horizontal_diff(N):-
    horizontal_colour(R,_),
    horizontal_colour(R2,_),
    R2 > R,
    N is R2 - R.

vertical_diff(N):-
    vertical_colour(C,_),
    vertical_colour(C2,_),
    C2 > C,
    N is C2 - C.

output_colour(R,C,Colour):-
    vertical_colour(Cstart, Colour),
    vertical_diff(VD),
    col(C),
    row(R),
    C >= Cstart,
    0 is ((C-Cstart) rem (2 * VD)).

output_colour(R,C,Colour):-
    horizontal_colour(Rstart, Colour),
    horizontal_diff(VD),
    row(R),
    col(C),
    R >= Rstart,
    0 is ((R-Rstart) rem (2 * VD)).

