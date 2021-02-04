Memorandum
-
DATE: February 4th, 2021

TO: Manager

FROM: Brandon Nzukie, Blake Hatch

SUBJECT: "Traveller Server Specification Implementation"

 1. The other team implemented our specification almost fully truthfully, with the exception of some minor differences
 in what the functions take in. However, I think given that they preserved the same functions and kept the data
 structure design identical, that the minor differences do not detract from how precisely they followed our 
 specification. 
 2. As the data and function design are practically identical between our specification and their implementation, it
 would be extremely easy to integrate with our client module. The main work would be changing from a class structure in
 our client to a functional one where the graph is accessible by our client either through storing it there or exporting
 from the received file.
 3. If our specification implied a class structure instead of functional and the team implemented as truthfully as they
  did with our current specification, we could have plugged it into our client with almost no effort, it would just 
  entail changing one or two inputs that the interface methods expected.