from operator import imod
from unicodedata import bidirectional
from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),                            # A is a knight or a knave...
    Not(And(AKnight, AKnave)),                      # ...but not both
    Implication(AKnight, And(AKnight, AKnave)),     # If A is a Knight, then the statement is true
    Implication(AKnave, Not(And(AKnight, AKnave)))  # If A is a Knave, then the statement is false
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),                # A is a knight or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),                # B is a knight or a knave but not both
    Implication(AKnight, And(AKnave, BKnave)),                          # Statement by A is true if A is a knight
    Implication(AKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave))) # Statement by A is false if A is a knave
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),                    # A is a knight or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),                    # B is a knight or a knave but not both
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),   # If A is a knight then A and B are both either Knights or Knaves
    Implication(AKnave, Or(And(AKnave, BKnight), And(AKnight, BKnave))),    # If A is a knave then A and B are Knight and Knave or vice versa
    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),   # If B is a knight then A and B are Knight and Knave or vice versa
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))     # If B is a knave then A and B are both either Knights or Knaves
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),    # A is a knight or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),    # B is a knight or a knave but not both
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),    # C is a knight or a knave but not both
    
    # Sentence 3
    Implication(BKnight, CKnave),                           # If B is a Knight then C is a Knave
    Implication(BKnave, CKnight),                           # If B is a Knave then C is a Knight
    
    # Sentence 4
    Implication(CKnight, AKnight),                          # If C is a Knight then A is a Knight
    Implication(CKnave, AKnave),                            # If C is a Knave then A is a Knave

    # Sentence 2 and Sentence 1
    Implication(BKnight, And(                               # If B is a knight then A said "I am a knave"
                            Implication(AKnight, AKnave),   # If A was a knight then A is a knave
                            Implication(AKnave, AKnight))   # If A was a knave then A is a knight
    ),

    Implication(BKnave, And(                                # If B is a knave then A said "I am a knight"
                            Implication(AKnight, AKnight),  # If A was a knight then A is a knight
                            Implication(AKnave, AKnave))    # If A was a knave then A is a knave.
    )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
