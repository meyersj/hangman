import urllib2

from scenes import Scenes


randomword = "http://randomword.setgetgo.com/get.php?len={0}"


def get_word(length=10):
    response = urllib2.urlopen(randomword.format(length))
    word = response.read()
    return word


class Hangman(object):
    
    def __init__(self, scenes, level):
        # word length accepted by randomword api must be between 3 and 30
        # level 1 = 4 char
        # level 2 = 6 char
        # ...
        # level 5 = 12 char
        length = 2 * (int(level) + 1)
        self.word = get_word(length).lower()
        self.matched = [ "_" for i in range(0, len(self.word)) ]
        self.incorrect = []
        self.scenes = scenes
        self.status = 0 # corresponds to index of current scene

    def start(self):
        print "You have 10 incorrect guesses before your man is hanged"
        print "Good Luck!", "\n"
        print self.scenes[self.status]
        self.status += 1

    def take_turn(self):
        # if we are at last scene the player has lost
        # return false to terminate game
        if self.status == len(self.scenes) - 1:
            print self.scenes[self.status]
            print "You lose. Loser.\n"
            print "Actual word was {0}".format(self.word), "\n"
            return False
        
        print "\nIncorrect: ", " ".join(self.incorrect)
        print "\nMatched: ", " ".join(self.matched), "\n"
        return self.__guess_handler(UI.guess_letter())

    def __guess_handler(self, guess):
        # if guess is string WIN user wants to guess actual word
        # check their guess, print response then exit game
        if guess == "WIN":
            word = UI.guess_word()
            self.__winner(word.lower())
            return False
        
        # check if guess matches any characters and update 
        guess = guess.lower()
        if guess in self.word:
            print "Letter {0} found in word. Good Job!".format(guess)
            for i, letter in enumerate(self.word):
                if letter == guess: self.matched[i] = guess
        else:
            print "WRONG! You're hanging him."
            print self.scenes[self.status]
            self.incorrect.append(guess)
            self.status += 1
        return True

    def __winner(self, word_guess):
        winner = "You WON!!!!!!\n"
        loser = "You're guess {0} was wrong, actual word was {1}. Loser"
        if word_guess == self.word: 
            msg = winner
        else:
            msg = loser.format(word_guess, self.word) + "\n"
        print msg


class UI(object):

    @staticmethod
    def guess_letter():
        guess = raw_input("Guess a letter (or enter 'WIN' to try and guess word): ")
        if guess == "WIN":
            print
            return guess
        while len(guess) != 1:
            guess = raw_input("Enter only a single character or 'WIN', re-enter: ")
            if guess == "WIN":
                break
        print
        return guess
    
    @staticmethod
    def guess_word():
        valid = ["y", "n"]
        correct = False
        while not correct:
            guess = raw_input("\nEnter your guess: ")
            print "You entered: {0}".format(guess)
            response = raw_input("Is that correct? [y,n]: ")
            while response not in valid:
                response = raw_input("Response must by 'y' or 'n', re-enter: ")
            if response == "y": correct = True
        print
        return guess

    @staticmethod
    def difficulty():
        valid = ["1", "2", "3", "4", "5"]
        level = raw_input("Select a difficulty level [1,2,3,4,5]: ")
        while level not in valid:
            level = raw_input("Level must be number from 1 to 5, re-enter: ")
        print
        return level

    @staticmethod
    def play_again():
        valid = ["y", "n"]
        response = raw_input("Play again? [y,n]: ")
        while response not in valid:
            response = raw_input("Response must by 'y' to play again or 'n' to exit: ")
        print
        return response


def runner():
    level = UI.difficulty()
    hangman = Hangman(Scenes, level)
    hangman.start()
    while hangman.take_turn(): pass
        

def main():
    again = "y"
    while again == "y":
        runner()
        again = UI.play_again()

if __name__ == "__main__":
    main()
