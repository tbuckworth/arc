all_rows(Rs):-
    setof(R, C^Colour^input_colour(R,C,Colour), Rs).

all_cols(Cs):-
    setof(C, R^Colour^input_colour(R,C,Colour), Cs).

row(R):-
    all_rows(Rs),
    member(R,Rs).

col(C):-
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
    Min1 is min(L, Min0),
    min(Ls, Min1, Min).

max([L|Ls], Max):-
    max(Ls, L, Max).

max([], Max, Max).
max([L|Ls], Max0, Max) :-
    Max1 is max(L, Max0),
    max(Ls, Max1, Max).

