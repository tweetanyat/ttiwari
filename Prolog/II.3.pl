/*The Englishman lives in the red house.
The Spaniard owns a dog.
The Norwegian lives in the first house
Kools are smoked in the yellow house.
Chesterfields are smoked next to where the fox is kept.
The Norwegian lives next to the blue house.
The Old Gold Smoker owns snails
The Lucky Strike smoker drinks orange juice
The Ukrainian drinks tea
The Japanese smokes Parliaments
The Kools smoker lives next to where the house is kept
Coffee is drunk in the green house
The green house is to the immediate right of the ivory house
Milk is drunk in the middle house
*/

problem(Water, Zebra) :-
%A board that contains the five variables over five categories.
%The categories are Color, Nationality, Pet, Drinks and Smokes 
%We will look for conditions throughout the code and fill in 
%appropriate entries.
	House = [[Col1, Nat1, Pet1, Dri1, Smo1],
		 [Col2, Nat2, Pet2, Dri2, Smo2],
		 [Col3, Nat3, Pet3, Dri3, Smo3],
		 [Col4, Nat4, Pet4, Dri4, Smo4],
		 [Col5, Nat5, Pet5, Dri5, Smo5]],
		 
	%Translate the sentences of the problem into equations one by one.
	%All member functions.
	member([red, englishman, _, _, _], House),
	member([_, spaniard, dog, _, _], House),
	member([green, _, _, coffee, _], House),
	member([_, ukranian, _, tea, _], House),
	member([_, _, snails, _, oldgold], House),
	member([yellow, _, _, _, kools], House),
	member([_, _, _, orangejuice, luckstrike], House),
	member([_, japanese, _, _, parliaments], House),
	member([_, Who_water, _, water, _], House),
	member([_, Who_zebra, zebra, _, _], House),
	
	%All to_right functions
	to_right([green, _, _, _, _], [ivory, _, _, _, _], House),
	Dri3 = milk,
	Nat1 = norwegian,
	
	(to_right([_, _, fox, _, _], [_, _, _, _, chesterfields], House);
	to_right([_, _, _, _, chesterfields], [_, _, fox, _, _], House)),
	(to_right([_, _, horse, _, _], [_, _, _, _, kools], House);
	to_right([_, _, _, _, kools], [_, _, horse, _, _], House)),
	(to_right([_, norwegian, _, _, _], [blue, _, _, _, _], House);
	to_right([blue, _, _, _, _], [_, norwegian, _, _, _], House)),
	
	%Print solution
	write(Who_water), write(' drinks water'),write(' and '),write(Who_zebra),write(' owns a zebra.').

%to_right function definition
to_right(H1, H2, [H2,H1|_]).
to_right(H1, H2, [_|T]) :-
	to_right(H1,H2,T).	


