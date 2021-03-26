# Milestone 6 - Refactoring Report

**Team members:** Brandon Nzukie, Blake Hatch

**Github team/repo:** Enesseand


## Plan

- Add docstrings for all of our functions.
- Clean up messy commented out debugging lines/old code.
- Clean up object modification code to make clearer.
- Make modifying objects consistent with just changing individual components instead of replacing entire object 
(Specifically gamestate is unecessarily replaced each time).
- Privatize functions that shouldn't be public to restrict over-access to the internal code.
- Abstract some code functionality, too much reused code especially for modifying and creating objects.
- Clean up tests, some single tests cover too many conditions and object instantiation for tests is very cluttered 
which makes it confusing what to test for.
- Make code more adaptable and flexible for potential requirements changes from the professors. This could be achieved 
through making functions more generic, easily allowing extended functionality through smart use of default 
argument values/behavior. For example, if you get a level it would have default rooms or use custom you provide, this
also has the side-effect of making instantiating objects for tests far easier.


## Changes

- Changed the way getting neighboring rooms from either a hallway, room, or origin works by extracting the functionality
into it's own utility function.
- Privatized functions to better restrict access to internal code.
- Clean up messy commented code.
- Add docstrings for all of our functions.


## Future Work

- Make tests neater.
- Abstracting code functionality.
- Makes code more adaptable to future changes from the professors.


## Conclusion

We hope that through this refactoring that we have a stronger base to build on for the last milestones and that it will
be more ready for the final task of wrapping everything up into a working game. 