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

output_colour(Row,Column,black):-
    row(Row),
    col(Column).
