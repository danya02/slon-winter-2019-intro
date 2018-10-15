# TL;DR: 42
AKA "The Borken Web Form"

Well, this should be easy, right? I mean, just copy the equation into [an RPN calculator](https://gist.github.com/jpcaruana/3973495), and then just select the answer in the web form...

Huh. The answer is `42`, but that answer's not on the web form... Oh well, I'll just select the first one, and... it's obviously wrong.

The other answers don't do anything either... It's probably just that the person who wrote this forgot to add the correct answer. How about I just fire up the network analyser and create a POST request with the correct answer, and see if... wait, ***it actually worked???***

Kidding aside, the main clue that something weird was going on was that, rather than sending the answer the usual way, the task requests that one use a webform for this. Either way, I'd say it's a pretty neat trick question.
