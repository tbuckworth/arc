

row(R):-
    input_colour(R,_,_).

column(C):-
    input_colour(_,C,_).

nrow(NR):-
    row(NR),
    row(R),
    \+ R > NR.

ncol(NC):-
    col(NC),
    col(C),
    \+ C > NC.

vertical_colour(C,Colour):-
    input_colour(R,C,Colour),
    R is 0,
    \+ Colour = black.

vertical_colour(C,Colour):-
    nrow(NR),
    input_colour(NR,C,Colour),
    \+ Colour = black.


horizontal_colour(R,Colour):-
    input_colour(R,C,Colour),
    C is 0,
    \+ Colour = black.

horizontal_colour(R,Colour):-
    ncol(NC),
    input_colour(R,NC,Colour),
    \+ Colour = black.


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

remainder(N,D,R):-
    integer(X),
    R is N - X * D.

output_colour(_,C,Colour):-
    vertical_colour(Cstart,Colour),
    column(C),
    vertical_diff(VD),
    C >= Cstart,
    VDtwo is 2 * VD,
    remainder(C-Cstart, VDtwo, R),
    R == 0.

output_colour(R,_,Colour):-
    horizontal_colour(Rstart,Colour),
    row(R),
    horizontal_diff(VD),
    R >= Rstart,
    VDtwo is 2 * VD,
    remainder(R-Rstart, VDtwo, Rem),
    Rem == 0.


output_colour(R,C,black):-
    \+ output_colour(R,C,_).

