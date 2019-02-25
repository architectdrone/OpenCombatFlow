# OpenCombatFlow

Hello, and welcome to OpenCombatFlow! I am Owen Mellema, and I am pleased to present you with this package.


## Usage (As of 1.0)

Using OpenCombatFlow (also known as OCF) is easy. All that is required to make a small game is contained within the module "character". The workflow looks something like this:

1. Create a new character class that extends the base Character class.

2. Implement getActionBlock and getReactionBlock. (If you forget, a NotImplementedError will be raised.)

3. Create a new combatHandler object.

4. Add objects from your new character class to the combatHandler, using the addCharacter() method.

5. Use turn() to increment through the characters.

Everything else (how attacks work, how results will be shown, etc) is up to you.


## Blocks

In OCF, I use a system of structured dictionaries to store and pass information between objects. I think this is useful for a variety of reasons. The required structure of these blocks (as I call them) is detailed in a document called "DSD.txt", which can be found in the directory where OCF is installed. You can also access it on my website (ENTER URL HERE). "MANDATORY" means that the tag musgt be included, "NOT MANDATORY" means that it is optional, and "CONDITIONALLY MANDATORY" means that it is mandatory only in certain circumstances, as indicated by the description.


## Dice

Features involving dice can also be implemented, using dice strings. A dice string is an expression that indicates a number of dice, modifiers, and conditional statements. An example dice string is "1d4+5>6", which means "roll one four sided die, add five, and see if the result is greater than six." (The results of a failed conditional depend on the circumstances, but usually it defaults to returning 0.) To use dice strings directly, import the dice module from OpenCombatFlow, and use the evaluate() function. Additionally, several fields in the DSD specify that they are "Dice Safe" (abbreviated "DS"), meaning that either dice strings  or integers can be passed to them. For the format of Dice Strings, please view "DiceStringFormat.txt" in the directory where OCF is installed, or view the page on my website (ENTER URL HERE).


## Caveat

This is the first package I have ever made for python, so if I mess up, I apologize. Python's module system is both elegant and arcane. Please give me any feedback you might have on the github repo (https://github.com/architectdrone/OpenCombatFlow). Please be sure to remember the human when/if you do. :)


## Links

The OpenCombatFlow Website: https://architectdrone.github.io/openCombatFlow/index.html

The Repo: https://github.com/architectdrone/OpenCombatFlow


## Conclusion

Have fun, and happy hacking!