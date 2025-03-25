import random
import time
import argparse

# Set the cosmic alignment of our random numbers
random.seed(0)


class Die:
    """A haunted die"""

    def roll(self):
        return random.randint(1, 6)


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.soul_intact = True

    def add_points(self, points):
        # Each point is a fragment of your soul
        self.score += points
        if points > 15:
            print(f"{self.name} feels a slight chill as {points} soul fragments are collected.")
        else:
            print(f"{self.name} adds {points} points. Total: {self.score}")


class HumanPlayer(Player):
    """You poor, lost soul"""

    def take_turn(self, die):
        turn_score = 0
        print(f"\n{self.name}'s turn begins...s.")

        while True:
            # Cast the die into the void
            roll = die.roll()
            print(f"{self.name} rolled a {roll}" + (" - THE DIE BETRAYS YOU!" if roll == 1 else ""))

            # The cruel '1' that ends all hopes and dreams
            if roll == 1:
                print(f"The shadows laugh as {self.name} loses all points this turn.")
                return 0

            # Another step deeper into temptation
            turn_score += roll
            print(f"Turn score: {turn_score} (Total would be: {self.score + turn_score})")

            # The eternal question: greed or safety?
            choice = input("Tempt fate again (r) or cling to your meager winnings (h)? ")
            if choice.lower() == 'h':
                self.add_points(turn_score)
                return turn_score


class DemonicOpponent(Player):
    """It's not cheating if you're supernatural"""

    def __init__(self, name, greed=15):
        super().__init__(name)
        self.greed = greed
        self.victims = 0

    def take_turn(self, die):
        turn_score = 0
        print(f"\n{self.name}'s eyes gleam with otherworldly power.")

        while True:
            # Even demons must abide by the rules of the die
            roll = die.roll()
            print(f"{self.name} rolled a {roll}")

            if roll == 1:
                print(f"{self.name} hisses in frustration as their turn yields nothing.")
                return 0

            turn_score += roll
            print(f"{self.name} has accumulated {turn_score} points this turn.")

            # Demons have simple strategies
            if turn_score >= self.greed:
                self.add_points(turn_score)
                if turn_score > 12:
                    self.victims += 1
                    print(f"{self.name} has claimed {self.victims} souls in this game.")
                return turn_score

            print(f"{self.name} hungers for more points...")


# NEW CLASS: Computer Player with the required strategy
class ComputerPlayer(Player):
    """A cold, calculating machine player"""
    
    def take_turn(self, die):
        turn_score = 0
        print(f"\n{self.name}'s circuits calculate the optimal move...")
        
        while True:
            roll = die.roll()
            print(f"{self.name} rolled a {roll}")
            
            if roll == 1:
                print(f"{self.name} processes an error as its turn yields nothing.")
                return 0
                
            turn_score += roll
            print(f"{self.name} has accumulated {turn_score} points this turn.")
            
            # Strategy: hold at min(25, 100-score)
            threshold = min(25, 100 - self.score)
            if turn_score >= threshold:
                self.add_points(turn_score)
                print(f"{self.name} executes 'hold' protocol at threshold {threshold}.")
                return turn_score
                
            print(f"{self.name} calculates additional risk as acceptable...")


# NEW CLASS: Player Factory
class PlayerFactory:
    """Creates different types of players"""
    
    @staticmethod
    def create_player(player_type, name, difficulty=3):
        """Factory method for creating players"""
        if player_type.lower() == "human":
            print(f"A mortal named {name} joins the cosmic game...")
            return HumanPlayer(name)
            
        elif player_type.lower() == "computer":
            print(f"A calculating machine named {name} enters the contest...")
            return ComputerPlayer(name)
            
        elif player_type.lower() == "demon":
            demon_names = ["BLese", "Asmodan", "Lilith", "Mephiston", "Abadon", "Grandpa"]
            if name == "random":
                name = random.choice(demon_names)
                
            greed_level = 10 + (difficulty * 2)
            print(f"From the shadows emerges {name}, your otherworldly opponent.")
            return DemonicOpponent(name, greed_level)
            
        else:
            raise ValueError(f"Unknown player type: {player_type}")


class AccursedGame:
    """This isn't just a game - it's a binding contract"""

    def __init__(self, mortal, demon):
        self.mortal = mortal
        self.demon = demon
        self.current_player = self.mortal  # Mortals always go first (disadvantage)
        self.die = Die()
        self.winning_score = 100

    def switch_player(self):
        # The cosmic pendulum swings
        self.current_player = self.demon if self.current_player == self.mortal else self.mortal

    def check_winner(self):
        # Has someone collected enough soul fragments?
        if self.mortal.score >= self.winning_score:
            return self.mortal
        elif self.demon.score >= self.winning_score:
            return self.demon
        return None
        
    def play_turn(self):
        """Play one turn and check for winner"""
        self.current_player.take_turn(self.die)
        
        winner = self.check_winner()
        if not winner:
            self.switch_player()
            
        return winner

    def play_game(self):
        print("╔════════════════════════════════════╗")
        print("║  THE ACCURSED GAME OF SKULL DICE!  ║")
        print("╚════════════════════════════════════╝")
        print(f"First to {self.winning_score} soul fragments will claim the other's essence!")

        winner = None
        while not winner:
            self.current_player.take_turn(self.die)
            
            winner = self.check_winner()
            if winner:
                print(f"\n☠️  {winner.name} HAS WON WITH {winner.score} POINTS! ☠️")
                if winner == self.demon:
                    print(f"Poor {self.mortal.name}... another soul claimed by {self.demon.name}.")
                else:
                    print(f"Impressive, {self.mortal.name}! You've bested a creature of the void!")
                break
            
            self.switch_player()


# NEW CLASS: Timed Game Proxy
class TimedGameProxy:
    """A proxy that adds a time limit to the accursed game"""
    
    def __init__(self, player1, player2, time_limit=60):
        """Create the proxy with a wrapped game instance"""
        self.game = AccursedGame(player1, player2)
        self.time_limit = time_limit  # Time limit in seconds
        self.start_time = None
        
    def check_winner(self):
        """Check for a winner by score or time expiration"""
        # First check normal win condition
        winner = self.game.check_winner()
        if winner:
            return winner
            
        # Then check time limit
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.time_limit:
            return self._determine_time_winner()
            
        return None
        
    def _determine_time_winner(self):
        """Determine winner when time expires"""
        print(f"\n⏱️ TIME'S UP! The cosmic clock has reached {self.time_limit} seconds!")
        
        if self.game.mortal.score > self.game.demon.score:
            return self.game.mortal
        elif self.game.demon.score > self.game.mortal.score:
            return self.game.demon
        else:
            # Handle tie case
            print("The cosmic forces declare a stalemate. Both players survive... for now.")
            return "TIE"
            
    def switch_player(self):
        """Delegate to the wrapped game"""
        self.game.switch_player()
        
    def play_turn(self):
        """Play one turn and check time"""
        elapsed_time = time.time() - self.start_time
        print(f"Time remaining: {self.time_limit - elapsed_time:.1f} seconds")
        
        winner = self.game.play_turn()
        
        # Check time after turn
        if not winner:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.time_limit:
                return self._determine_time_winner()
                
        return winner
    
    def play_game(self):
        """Play the timed version of the game"""
        print("╔════════════════════════════════════╗")
        print("║  THE TIMED GAME OF SKULL DICE!     ║")
        print("╚════════════════════════════════════╝")
        print(f"First to {self.game.winning_score} soul fragments will claim the other's essence!")
        print(f"⏱️ But beware! You have only {self.time_limit} seconds to determine a victor! ⏱️")
        
        self.start_time = time.time()
        winner = None
        
        while not winner:
            winner = self.play_turn()
            
            if winner == "TIE":
                print(f"\n⏱️ TIME'S UP - IT'S A DRAW! ⏱️")
                print(f"Mortal: {self.game.mortal.score} points | Demon: {self.game.demon.score} points")
                break
                
            if winner:
                print(f"\n☠️  {winner.name} HAS WON WITH {winner.score} POINTS! ☠️")
                if winner == self.game.demon:
                    print(f"Poor {self.game.mortal.name}... another soul claimed by {self.game.demon.name}.")
                else:
                    print(f"Impressive, {self.game.mortal.name}! You've bested a creature of the void!")
                break
        
        elapsed = time.time() - self.start_time
        print(f"Total game time: {elapsed:.1f} seconds")


# Modified main function that uses factory and arguments
def main():
    """Main function with argument handling"""
    parser = argparse.ArgumentParser(description="Play the Accursed Game of Pig")
    parser.add_argument("--player1", choices=["human", "computer", "demon"], default="human",
                      help="Type of player 1 (human, computer, or demon)")
    parser.add_argument("--player2", choices=["human", "computer", "demon"], default="demon",
                      help="Type of player 2 (human, computer, or demon)")
    parser.add_argument("--timed", action="store_true", help="Enable timed game mode (1 minute limit)")
    parser.add_argument("--p1name", default="Mortal", help="Name for player 1")
    parser.add_argument("--p2name", default="random", help="Name for player 2")
    parser.add_argument("--difficulty", type=int, choices=range(1, 6), default=3,
                      help="Difficulty level (1-5) for computer/demon players")
    args = parser.parse_args()
    
    # Create players using the factory
    player1 = PlayerFactory.create_player(args.player1, args.p1name, args.difficulty)
    player2 = PlayerFactory.create_player(args.player2, args.p2name, args.difficulty)
    
    # Create the appropriate game type
    if args.timed:
        print("\nThe cosmic clock begins ticking... you have ONE MINUTE to determine a victor!")
        game = TimedGameProxy(player1, player2)
    else:
        game = AccursedGame(player1, player2)
    
    # Let the cosmic game begin!
    game.play_game()
    
    print("\nThe game is over, but remember your choices...")


# Still keep the original main code for backward compatibility
if __name__ == "__main__":
    import sys
    
    # If command line arguments are provided, use the new main function
    if len(sys.argv) > 1:
        main()
    else:
        # Otherwise, use the original code
        print("Welcome, mortal, to a game where dice are more than just plastic cubes.")

        # Who dares to play?
        mortal_name = input("By what name shall the cosmos know you? ")
        mortal = HumanPlayer(mortal_name)

        # Your demonic opponent emerges
        demon_names = ["BLese", "Asmodan", "Lilith", "Mephiston", "Abadon", "Grandpa"]
        demon_name = random.choice(demon_names)
        print(f"\nFrom the shadows emerges {demon_name}, your otherworldly opponent.")

        # How strategic is your opponent?
        try:
            difficulty = int(input("How cunning is your opponent? (1-5, higher = more devious): "))
            greed_level = 10 + (difficulty * 2)  # Higher difficulty = higher greed threshold
        except:
            print("Your indecision has been noted.")
            greed_level = random.randint(10, 20)

        demon = DemonicOpponent(demon_name, greed_level)

        # Let the cosmic game begin!
        game = AccursedGame(mortal, demon)
        game.play_game()

        print("\nThe game is over, but remember your choices...")
