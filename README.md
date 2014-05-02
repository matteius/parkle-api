parkle-api
==========

Python Farkle implementation (alt) w/ tests and API in dev.

The how to play part is not finished yet, but if you read the recursive scoring algorithm it is like reading the rules of the game, and the test logic proves it is correct. Better than I can say for practically any other open source Farkle implementation.

There is another parkle implementation worth mentioning, which CLI interface and AI support though I found the scoring algorithm lacking.   You can find that prior work here:  https://github.com/Zolmeister/parkle

Current and Future dev:
* AI sub-system (Users should be able to write their own AI class logic)
* API + redis state utils (Scalable API implementation)
* Client implementations (for playing the game)
