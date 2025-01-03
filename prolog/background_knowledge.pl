% Students must define row/1, col/1 and output_colour/3.

output_with_default(Row, Column, Colour) :-
    row(Row),
    col(Column),
    output_colour(Row, Column, Colour).

output_with_default(Row, Column, black) :-
    row(Row),
    col(Column),
    \+ output_colour(Row, Column, _).

print_results([]).
print_results([(R, C, Colour) | Rest]) :-
    write('output_colour('),
    write(R), write(','),
    write(C), write(','),
    write(Colour), write(').'), nl,
    print_results(Rest).

print_results :-
    setof((R, C, Colour), R^C^Colour^output_with_default(R, C, Colour), Results),
    print_results(Results).
