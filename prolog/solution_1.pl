

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

vertical_colour(C,Colour):-
    input_colour(R,C,Colour),
    R is 0,
    Colour \= black.

vertical_colour(C,Colour):-
    row(R),
    input_colour(R,C,Colour),
    Colour \= black.

horizontal_colour(R,Colour):-
    input_colour(R,C,Colour),
    C is 0,
    Colour \= black.

horizontal_colour(R,Colour):-
    column(C),
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
    column(C),
    row(R),
    C >= Cstart,
    0 is ((C-Cstart) rem (2 * VD)).

output_colour(R,C,Colour):-
    horizontal_colour(Rstart, Colour),
    horizontal_diff(VD),
    row(R),
    column(C),
    R >= Rstart,
    0 is ((R-Rstart) rem (2 * VD)).


output_colour(R,C,black):-
    \+ output_colour(R,C,_).

%set_prolog_flag(print_length, infinite).
%setof([R,C,Colour], R^C^Colour^output_colour(R,C,Colour), Cs).


%written:-
%    output_colour(R,C,Colour),
%    write({"output_colour("+R+","+C+","+Colour+").\n"}).

forall(P, Q):-
    \+ (P, \+ Q).

print_forall :-
    forall(output_colour(R, C, Colour),
           (write('output_colour('),
            write(R), write(', '),
            write(C), write(', '),
            write(Colour), write(').'),
            nl)).

print_setof :-
    setof((R, C, Colour), R^C^Colour^output_colour(R, C, Colour), Results),
    print_results(Results).

print_results([]).
print_results([(R, C, Colour) | Rest]) :-
    write('output_colour('),
    write(R), write(', '),
    write(C), write(', '),
    write(Colour), write(').'), nl,
    print_results(Rest).














