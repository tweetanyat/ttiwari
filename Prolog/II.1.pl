%moves:
%two cannibals go from left to right
move([LCan,LMiss,left,RCan,RMiss],[LCan_new,LMiss,right,RCan_new,RMiss]):-
	LCan_new is LCan-2,
	RCan_new is RCan+2,
	LCan_new>=0, LMiss>=0, RCan_new>=0, RMiss>=0,
	(LMiss>=LCan_new ; LMiss=0),
	(RMiss>=RCan_new ; RMiss=0).

%two missionaries go from left to right
move([LCan,LMiss,left,RCan,RMiss],[LCan,LMiss_new,right,RCan,RMiss_new]):-
	LMiss_new is LMiss-2,
	RMiss_new is RMiss+2,
	LCan>=0, LMiss_new>=0, RCan>=0, RMiss_new>=0,
	(LMiss_new>=LCan ; LMiss_new=0),
	(RMiss_new>=RCan ; RMiss_new=0).

%two cannibals go from right to left
move([LCan,LMiss,right,RCan,RMiss],[LCan_new,LMiss,left,RCan_new,RMiss]):-
	LCan_new is LCan+2,
	RCan_new is RCan-2,
	LCan_new>=0, LMiss>=0, RCan_new>=0, RMiss>=0,
	(LMiss>=LCan_new ; LMiss=0),
	(RMiss>=RCan_new ; RMiss=0).

%two missionaries go from right to left
move([LCan,LMiss,right,RCan,RMiss],[LCan,LMiss_new,left,RCan,RMiss_new]):-
	LMiss_new is LMiss+2,
	RMiss_new is RMiss-2,
	LCan>=0, LMiss_new>=0, RCan>=0, RMiss_new>=0,
	(LMiss_new>=LCan ; LMiss_new=0),
	(RMiss_new>=RCan ; RMiss_new=0).

%one cannibal goes from left to right
move([LCan,LMiss,left,RCan,RMiss],[LCan_new,LMiss,right,RCan_new,RMiss]):-
	LCan_new is LCan-1,
	RCan_new is RCan+1,
	LCan_new>=0, LMiss>=0, RCan_new>=0, RMiss>=0,
	(LMiss>=LCan_new ; LMiss=0),
	(RMiss>=RCan_new ; RMiss=0).

%one missionary goes from left to right
move([LCan,LMiss,left,RCan,RMiss],[LCan,LMiss_new,right,RCan,RMiss_new]):-
	LMiss_new is LMiss-1,
	RMiss_new is RMiss+1,
	LCan>=0, LMiss_new>=0, RCan>=0, RMiss_new>=0,
	(LMiss_new>=LCan ; LMiss_new=0),
	(RMiss_new>=RCan ; RMiss_new=0).

%one cannibal goes from right to left
move([LCan,LMiss,right,RCan,RMiss],[LCan_new,LMiss,left,RCan_new,RMiss]):-
	LCan_new is LCan+1,
	RCan_new is RCan-1,
	LCan_new>=0, LMiss>=0, RCan_new>=0, RMiss>=0,
	(LMiss>=LCan_new ; LMiss=0),
	(RMiss>=RCan_new ; RMiss=0).

%one missionary goes from right to left
move([LCan,LMiss,right,RCan,RMiss],[LCan,LMiss_new,left,RCan,RMiss_new]):-
	LMiss_new is LMiss+1,
	RMiss_new is RMiss-1,
	LCan>=0, LMiss_new>=0, RCan>=0, RMiss_new>=0,
	(LMiss_new>=LCan ; LMiss_new=0),
	(RMiss_new>=RCan ; RMiss_new=0).

%one missionary and one cannibal go from left to right
move([LCan,LMiss,left,RCan,RMiss],[LCan_new,LMiss_new,right,RCan_new,RMiss_new]):-
	LCan_new is LCan-1,
	LMiss_new is LMiss-1,
	RCan_new is RCan+1,
	RMiss_new is RMiss+1,
	LCan_new>=0, LMiss_new>=0, RCan_new>=0, RMiss_new>=0,
	(LMiss_new>=LCan_new ; LMiss_new=0),
	(RMiss_new>=RCan_new ; RMiss_new=0).

%one missionary and one cannibal go from right to left
move([LCan,LMiss,right,RCan,RMiss],[LCan_new,LMiss_new,left,RCan_new,RMiss_new]):-
	LCan_new is LCan+1,
	LMiss_new is LMiss+1,
	RCan_new is RCan-1,
	RMiss_new is RMiss-1,
	LCan_new>=0, LMiss_new>=0, RCan_new>=0, RMiss_new>=0,
	(LMiss_new>=LCan_new ; LMiss_new=0),
	(RMiss_new>=RCan_new ; RMiss_new=0).

%approach to find solution
path([LCan_1,LMiss_1,Dir_1,RCan_1,RMiss_1],[LCan_new,LMiss_new,Dir_2,RCan_new,RMiss_new],Visited,Moves) :-
	move([LCan_1,LMiss_1,Dir_1,RCan_1,RMiss_1],[LCan_3,LMiss_3,Dir_3,RCan_3,RMiss_3]),
	not(member([LCan_3,LMiss_3,Dir_3,RCan_3,RMiss_3],Visited)),
	path([LCan_3,LMiss_3,Dir_3,RCan_3,RMiss_3],[LCan_new,LMiss_new,Dir_2,RCan_new,RMiss_new],[[LCan_3,LMiss_3,Dir_3,RCan_3,RMiss_3]|Visited], [[[LCan_3,LMiss_3,Dir_3,RCan_3,RMiss_3],[LCan_1,LMiss_1,Dir_1,RCan_1,RMiss_1]] | Moves]).

path([LCan,LMiss,Dir,RCan,RMiss],[LCan,LMiss,Dir,RCan,RMiss],_,Moves):-
	result(Moves).

result([]) :- nl.
result([[Move1,Move2]|Moves]) :-
	result(Moves),
	write(Move2), write('.....'), write(Move1), nl.

solution :-
   path([3,3,left,0,0],[0,0,right,3,3],[[3,3,left,0,0]],_).

