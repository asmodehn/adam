Here we keep multiple reficitation of the language, in different models of computation.

These need to be very simple in their essence, yet support any kind of computation. Full abstraction is suitable.

To be useful, we need to have 3 fully abstract implementation, able to check each other, at least at a common level in the computation (atomic computation, current continuation, delimited continuation, complete computation).

The goal is bisimulation at the chosen level of compatibility. Error detection implies destruction of the broken interpreter, and reinitialization.
Multiple successive errors with the same model implies hardware failure (actual implementatied reification is considered always correct - and should be formally proven), and hardware failure should be worked around as possible...

Roadmap :

- Soon :
  - Idris VM + Interpreter implementations (with totality check as proof)
  - Elm VM + Interpreter implementation (with github pages as demo) 

- Later : 
  - dogfooding : Interpreters implementation in Adam
  - dogfooding : VMs implementation in Adam
