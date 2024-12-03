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

min([L|Ls], Min) :-
    min(Ls, L, Min).

min([], Min, Min).
min([L|Ls], Min0, Min) :-
    Min1 is min(L, Min0), %N.B.
    min(Ls, Min1, Min).

max([L|Ls], Max):-
    max(Ls, L, Max).

max([], Max, Max).
max([L|Ls], Max0, Max) :-
    Max1 is max(L, Max0), %N.B.
    max(Ls, Max1, Max).

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
    R > R2.

left_wall_unique(W):-
    setof(C, left_wall(C), L),
    min(L, W).

right_wall_unique(W):-
    setof(C, right_wall(C), L),
    max(L, W).

top_wall_unique(W):-
    setof(C, top_wall(C), L),
    min(L, W).

bottom_wall_unique(W):-
    setof(C, bottom_wall(C), L),
    max(L, W).


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
    R > RT,
    bottom_wall_unique(RB),
    R < RB,
    left_wall_unique(CL),
    C > CL,
    right_wall_unique(CR),
    C < CR.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_horizontal(R,CG),
    input_colour(R,CB,grey),
    CB < C,
    CB < CG.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_horizontal(R,CG),
    input_colour(R,CB,grey),
    CB > C,
    CB > CG.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_vertical(RG,C),
    input_colour(RB,C,grey),
    RB < R,
    RB < RG.

output_colour(R,C,teal):-
    row(R),
    column(C),
    gap_vertical(RG,C),
    input_colour(RB,C,grey),
    RB > R,
    RB > RG.
