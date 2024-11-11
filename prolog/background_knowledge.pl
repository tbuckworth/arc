print_results([]).
print_results([(R, C, Colour) | Rest]) :-
    write('output_colour('),
    write(R), write(','),
    write(C), write(','),
    write(Colour), write(').'), nl,
    print_results(Rest).

print_results :-
    setof((R, C, Colour), R^C^Colour^output_colour(R, C, Colour), Results),
    print_results(Results).
