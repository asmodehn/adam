While it is possible to represent everything with tables like for bool, it quickly becomes painful.

A better way is needed, even for a constructive representation based on possible values.

One could curry n argument functions, but it leads to an implosion in projection of a function along one of the arguments, so we just moved the complexity from inside the file to outside.
We should attempt to keep function complexity encapsulated in it,and therefore would prefer a more structure file syntax...

However we want to keep file syntax to a minimum ( ogdl style ) so it looks ilke we cannot avoid repeating the second argument...
