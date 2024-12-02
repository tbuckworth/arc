all_rows(Rs):-
    setof(R, C^Colour^input_colour(R,C,Colour), Rs).

all_cols(Cs):-
    setof(C, R^Colour^input_colour(R,C,Colour), Cs).

row(R):-
    all_rows(Rs),
    member(R,Rs).

column(C):-
    all_cols(Cs),
    member(C,Cs).

nrow(NR):-
    all_rows(Rs),
    length(Rs, NR).

ncol(NC):-
    all_cols(Cs),
    length(Cs, NC).


min(A, B, B):-
    A < B.

min(B, A, B):-
    A >= B.
min([Min], Min).

min([H|T], Min):-
    min(T, MinT),
    min(H, MinT, Min).



left_wall(C):-
    input_colour(_,C,grey),
    input_colour(_,C2,grey),
    C2 > C.

right_wall(C):-
    input_colour(_,C,grey),
    input_colour(_,C2,grey),
    C2 < C.

top_wall(R):-
    input_colour(R,_,grey),
    input_colour(R2,_,grey),
    R < R2.

bottom_wall(R):-
    input_colour(R,_,grey),
    input_colour(R2,_,grey),
    R2 > R.

left_wall_unique(W):-
    setof(C, left_wall(C), L),
    min(L, W).

right_wall_unique(W):-
    setof(C, right_wall(C), L),
    min(L, W).

top_wall_unique(W):-
    setof(C, top_wall(C), L),
    min(L, W).

bottom_wall_unique(W):-
    setof(C, bottom_wall(C), L),
    min(L, W).


gap_horizontal(R,C):-
    input_colour(R,C,black),
    RT is R + 1,
    input_colour(RT,C,grey),
    RB is R - 1,
    input_colour(RB,C,grey).

gap_vertical(R,C):-
    input_colour(R,C,black),
    CT is C + 1,
    input_colour(R,CT,grey),
    CB is C - 1,
    input_colour(R,CB,grey).


output_colour(R,C,grey):-
    input_colour(R,C,grey).

output_colour(R,C,teal):-
    row(R),
    column(C),
    top_wall_unique(RT),
    R < RT,
    bottom_wall_unique(RB),
    R > RB,
    left_wall_unique(CT),
    C > CT,
    right_wall_unique(CB),
    C < CB.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_horizontal(R,CG),
    CG =< C,
    input_colour(R,CL,grey),
    CL < C.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_horizontal(R,CG),
    CG >= C,
    input_colour(R,CL,grey),
    CL > C.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_vertical(RG,C),
    RG =< R,
    input_colour(RB,C,grey),
    RB < R.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_vertical(RG,C),
    RG >= R,
    input_colour(RB,C,grey),
    RB > R.
