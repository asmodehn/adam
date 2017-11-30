# adam
Programming designed for machines

Bullet points in random order

- when machine can program, humans only need to be able to read/visualize the codefor it. It is a language for machine, more than it is for humans. humans only need to be able to understand it.
- if human eventually has to generate code, machine can refuse anything that is 'invalid syntax', so even the interface to program only allow valid construct.
- when both human and machine can write programs, while potentially representing two different semantics, there need to be a referential semantics. Math and category theory seems to be able to provide such a referential semantics,as well as a practical graphical representation.


Category Theory

- A monad is just a monoid of endofunctor
- Free Monad + Interpreter
- Input is a comonad
- language is a representation (or check yoneda lemma)
- Recursion is a fold
- algebraic data types
- F-algebras and catamorphisms



### Goals

 - Self correction (Error detection -> possible reparation -> implementation and verification)
 - Self optimization (Continous monitoring -> possible side effect improvement -> implementation and verification)
 - Self improvements (Continous monitoring -> possible functionality improvement -> implementation and verification)
 
### Background

 - Category Theory
 - Homotopy Type Theory
 - PCF / Kernel / Scheme / Haskell / ML / OCaml / Idris / Erlang / etc.
 - Dependent types
 - Definitional Interpreters
 - Reflection Towers
 - Interpreted Homoiconic to allow simple self modification 
 
### Terminology

Although we favorise Category Theory terminology, aliases will be introduced to avoid confusion with existing programming concepts in other areas...
 
### Chronology of choices

While progressing up and abstracting concepts, we strive to eliminate unnecessary constructs (that can be built later on).

Since we aim to focus on reification/reflection duality, we will focus on strings types only, and their possible manipulations, at first.
Also we will try to match the representation to something fitting the familiar file hierarchy.

##### Object : Set / Bag / Type / ... ? 

 - Statically enforced by language
   - No ordering (can be constructed later - list monad)
   - No structure (can be constructed later - categorical product)
   - No infinity (can be constructed later - induction)
   - Unicity or not doesnt seem to have an impact for now (maybe for determinism in morphisms)
   - Representation can be positive (elements) or negative (non elements from all possible)
 - Dynamically enforced by core components
   - Nothing just yet
 
 Choice : Finite Set, positive representation for bootstrapping
 Note : Types will be defined more precisely later to allow for homotopy (possibly using HoTT and typical category semantics)
 
 
 Initial Object : No element -> Not represented, just a way to select an Object
 Terminal Object : Singleton -> Object sink


##### Morphism : Procedure / Function / Curried Function / Mapping / ... ?

 - Statically enforced by language
   - Pure function (impurity can be constructed from it - monad / effects)
   - One input, one output to match categorical semantics
 - Dynamically enforced by core components
   - Totality is a goal for implementation verification, even if non-totality is allowed (interpreted as a partial definition of a function that should be completed)
   - Determinism seems better for now (as usually defined for Set Category) and indeterminism can be constructed from it. But it might be the otherway around (think quantum physics).
   - Representability is a challenge for core basic functions, for which we want to give a definitional interpreter
 
 Choice : Mapping with object elements as keys, positive representation for bootstrapping
 Note : This can also be interpreted as a Monad/Comonad (State/Store)
 
 Eval : Special Morphism, allowing interpretation of other morphisms. Representation requires product types. For elemental positive representation, Eval can be implemented just with pattern matching.
 
 
##### Functor : higher order function / mapping of morphisms / ... ?

 - Statically enforced by language
   - 
 - Dynamically enforced by core components
   - 

 Choice : Mapping with morphism mappings as keys, positive representation for bootstrapping
 Note : 
 
 Maybe Type Constructor : Representation ??? 
 
 Monad : Monoid of Endofunctor
 CoMonad : CoMonoid of Endofunctor
 
 ##### Natural Transformation : ?


# Orthogonaly : Implementation Braindump

## Python :
 
 - python "functions", that is routines, are too unrefined (high-level) for our implementation here, because they can take a long time, are indeterministically interruptible, and can be decomposed into coroutines + futures to separate the execution and the result retrieval into the original context.
 - having one eventloop per thread seems a good start, but we eventually need to manage input/output somehow, and relate that to terminal/pipes (TODO : check ptyprocess package) to be able to debug behaviour in details.
 - It seems the most basic concept is not a python routine, but something more refined, like a math function (memoizable), inside a never ending loop, that can only communicate to the outside via some logic loopholes (monads). This should allow us to tightly control a computation cost as well as result communication approximation.
 - Functions are composable inside a loop, but to get out of the loop, monadic functorial code should be used. Composing multiple loops is therefore a higher level construct, akin to a natural transformation or so... More study & experiments are required. 
 - there is no aiocurses package yet AFAIK, probably because of very incompatible design in libraries but we might think about producing one eventually to factor out what is not specific to adam from the python implementation.
 
 ## Various related ideas : 
 
 - Emily : https://www.youtube.com/watch?v=gMZsc3cvwKs , https://bitbucket.org/runhello/emily/wiki/Home
 - Next Great Functional Language : https://www.youtube.com/watch?v=buQNgW-voAg
 - Concatenative Languages : http://concatenative.org/wiki/view/Concatenative%20language
 - Kernel 