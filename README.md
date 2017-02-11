# demystifier
Inspired by an Internet joke about how the *P* and *S* in IoT 
stand for *privacy* and *security*, `demystifier` randomly decides
what the letters in (or **not in**) an acronym stand for. Use 
`demystifier` to learn what (typically) nonsensical meaning is
carried and/or omitted by your favorite initialism today!

# Examples

* Explain full acronym by default

    $ python demystifier.py ABC
    ABC stands for Actuarial Birdhouses Craved 

* Use letters not in set with -x

    $ python demystifier.py ABC -x
    ABC does not mean Ganged Libra Lambent

* Explain one letter with -o 

    $ python demystifier.py ABC -o
    The A in ABC stands for Avast

* Explain meaning of one letter not in set with -ox

    $ python demystifier.py IoT -ox
    The H in IoT stands for Harpsichord  
