from monster import Monster
import colorama as C
import cmd, platform, os

class Combat(cmd.Cmd):
    STRINGS = {
    'intro': 'You started a fight, Enemies are staring viciously at you!\n. . .',
    'win': 'VICTORY, You defeated all enemies!. . .',
    'lose': 'DEFEAT, You got beaten by enemies!\n. . .',
    'syntax_error': 'Oops! I dont understand',
    'unknown_enemy': "I can't see an enemy with such name!",
    'player_attack': "You punched",
    'enemy_death': "died",
    'prompt': 'Type <atk> to attack:',
    }

    # Color settings
    C.init()
    print(C.Fore.WHITE + C.Back.BLACK + C.Style.BRIGHT, end='')

    # Global constants
    LIST_SYMBOL = '*'
    PROMPT_SIGN = '#'


    def __init__(self, user, enemies):
        # cmd.Cmd initialization
        super().__init__()
        self.intro = input(self.STRINGS['intro'] + '\n')
        self.prompt = '{}{}\n'.format(self.PROMPT_SIGN, self.STRINGS['prompt'])

        # user/enemies variables
        self.user = user
        self.user_attack_msg = ''
        self.enemies = enemies
        self.no_of_enemies = len(enemies)
        self.enemies_dict = self.create_dictionary()
        self.enemies_attack_msg = ''

    # cmd.Cmd method overriding
    # Avoids repitition of last command
    def emptyline(self):
        self.display()
        pass

    # Error message for unknown commands
    def default(self, line):
        self.display()
        print(C.Back.RED + C.Fore.RED + '{}{} <{}>'.format(self.PROMPT_SIGN, self.STRINGS['syntax_error'], line))
        print(C.Back.BLACK + C.Fore.WHITE, end='')

    # Controls termination of Combat, win/lose msg
    def postcmd(self, stop, line):
        if not self.enemies_alive():
            print(C.Back.GREEN + C.Fore.GREEN , end='')
            input(self.PROMPT_SIGN + self.STRINGS['win'])
            return True

    # Pre/Post Loop functions
    def preloop(self):
        self.display()

    # Creates a dictionary that store Enemies and their corresponding names
    def create_dictionary(self):
        dict = {}
        for enemy in self.enemies:
            if enemy.alive:
                dict[enemy.name.lower()] = enemy
        return dict

    # Returns a string of alive enemy names
    def alive_enemy_names(self):
        names = ''
        for enemy in self.enemies:
            if enemy.alive:
                names += '  {} {}\n'.format(self.LIST_SYMBOL, enemy.name)
            else:
                pass
        return names

    # Are any enemy alive? True/False
    def enemies_alive(self):
        self.no_of_enemies = len(self.enemies)
        for enemy in self.enemies:
            if not enemy.alive:
                self.no_of_enemies -= 1
        if self.no_of_enemies > 0:
            return True
        else:
            return False

    # Attacks a chosen enemy
    def user_attack(self, enemy):
        self.user_attack_msg = C.Back.BLACK + C.Fore.YELLOW + "{}{} {}".format(self.PROMPT_SIGN, self.STRINGS['player_attack'], enemy.name)
        if (enemy.hp - self.user.dmg) <= 0:
            self.user_attack_msg += C.Back.BLACK + C.Fore.RED + "\n#{} {}".format(enemy.name, self.STRINGS['enemy_death'])
        self.user.attack(enemy)
    
    # All alive enemies attacks the user returning a hit string
    def enemies_attack(self):
        messages = ''
        for enemy in self.enemies:
            if enemy.alive:
                enemy.attack(self.user)
                hit_string = "!! {} {} you. ({}HP)\n".format(enemy.name, enemy.action, str(-enemy.dmg))
                messages += hit_string
        self.enemies_attack_msg = C.Back.BLACK + C.Fore.RED + messages
        
    # Displays the interface: All Enemies and user status
    def display(self, clear = True):
        if clear:
            self.clear()
        print(C.Back.BLACK + C.Fore.WHITE)
        self.user.show()
        for enemy in self.enemies:
            print(enemy.show())
        print(self.user_attack_msg) 
        print(self.enemies_attack_msg)
        print(C.Back.BLACK + C.Fore.WHITE)
         
    # Clears the terminal using the approperiate subshell command
    # for each terminal
    def clear(self, no_of_lines = 40):
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux' or 'Darwin':
            os.system('clear')

        print(C.Back.BLACK + '\n' * no_of_lines)

    # Cmd commands
    def do_atk(self, arg):
        """Attacks a specific enemy: atk <enemy name>"""
        self.display()
        while True:
            choice = input(self.PROMPT_SIGN + 'Type <enemy name>:\n' + self.alive_enemy_names() + '> ')
            self.enemies_dict = self.create_dictionary()
            try:
                target_enemy = self.enemies_dict[choice.lower()]
                self.user_attack(target_enemy)
                self.enemies_attack()
                self.display()
                return True
            except KeyError:
                print(C.Back.RED + C.Fore.RED, end='')
                input(self.PROMPT_SIGN + self.STRINGS['unknown_enemy'])
                self.display()
