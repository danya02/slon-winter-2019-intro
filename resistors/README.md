# TL;DR: 5 in series of (12 in parallel of 1ohm resistors)
AKA "We're gonna need a smaller box."

This does not use the least possible amount of resistors, but I'd still use it in a real-world application, because 1. it means each individual resistor's heat dissipation is lower, which means a lower required power rating, and 2. it's easier on the brain, which is helpful if the situation is so dire that I can't just go and buy a single precision resistor for the task.

First, we take 12 resistors in parallel, to get a 1/12ohm resistance per `Rp=1/((1/R1)+(1/R2)+...)`. Then, we connect five of these assemblies in series as per `Rs=R1+R2+...`.

Thus, we get a resistance of 5/12ohms, by using 60 1ohm resistors. Assuming [3.5mm body length](https://electronics.stackexchange.com/questions/129294/is-there-any-pattern-or-standard-to-through-hole-resistor-sizes) and 1mm for the solder joints on either side, and ignoring the volume for the wiring and the insulation tape required to prevent the assembly from shorting out, if using [optimum packing](https://en.wikipedia.org/wiki/List_of_shapes_with_known_packing_constant) without tiling the resistors vertically, you would be looking at a cuboid of [6 cm on the side](http://www.wolframalpha.com/input/?i=sqrt((60*(pi*(4mm)%5E2)%2F(pi%2Fsqrt(12))))), for a total volume of 18cm^3.
