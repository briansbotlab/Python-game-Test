# -*- coding: utf-8 -*-
from random import randrange

class Game:
    def __init__(self):
        self.__players = []
        self.__questions_category = []
        self.__num_of_questions = 0
        self.__question_box = []
        self.__current_category = 0
        self.__current_player = 0
        self.__game_start = False
        self.__penalty_box = Penalty_box()

    def list_all_players(self):  #for test
        for i in range(len(self.__players)):
            print(self.__players[i].get_purse_status())


    def add(self,player):
        self.__players.append(player)
        print(player.get_player_name() , "was added")
        print("They are player number %s"% len(self.__players))

    def __is_playable(self):
        if len(self.__players) <2:
            print("This game is two players required !")
        if self.__num_of_questions <= 0:
            print("You need to set the num of questions more than one !")
            print("now the num of questions is ", self.__num_of_questions)
        if len(self.__questions_category) <=0:
            print("You need to set the num of questions category more than one !")
            print("now the num of questions category is ", len(self.__questions_category))

        return len(self.__players) >=2 and (self.__num_of_questions >0) and len(self.__questions_category) >0

    def create_questions(self,num_of_questions):
        print("create qusetions!!")
        for j in self.__questions_category:  #j means category

            index_of_j = self.__questions_category.index(j)

            self.__question_box.append([])

            for i in range(num_of_questions): # i means the index of the category
                question =  Question(i,j)
                self.__question_box[index_of_j].append(question)

            print("The category ",j,"now has ", len(self.__question_box[index_of_j]) ,"questions")



    def set_num_of_questions(self, num):
        self.__num_of_questions = num
        print("The num of questions is " , self.__num_of_questions)


    def set_questions_category(self, *categories):
        for category in categories:
            self.__questions_category.append(category)

        print("Now, the questions category are ",self.__questions_category)

    def start_game(self):
        if(self.__is_playable() and not self.__game_start):
            print("game is playable!!")
            self.create_questions(self.__num_of_questions)
            self.__game_start = True
            print("game start !!")

    def roll(self , roll):
        current_player = self.__players[self.__current_player]
        print("%s is the current player"%current_player.get_player_name())
        print("They have rolled a %s"%roll)


        if self.__penalty_box.is_player_in_box(current_player):
            if roll % 2 != 0:
                self.__penalty_box.set_player_out_box(current_player)
                print("%s is getting out of the penalty box" %current_player.get_player_name())

        current_player.set_place(roll)
        print(type(current_player.get_place()))
        print(current_player.get_player_name(),
                      '\'s new location is ' ,
                      str(current_player.get_place()))
        
        self.__set_current_category(int(current_player.get_place()))
        #self.__current_category must be a integer
        self.__ask_question()


    def __set_current_category(self,current_place):
        self.__current_category = current_place % len(self.__questions_category)

    def __ask_question(self):
        ask_q = self.__question_box[self.__current_category].pop(0)
        print("Category :",ask_q.get_category())
        print("index :",ask_q.get_index())

    def was_correctly_answered(self):
        current_player = self.__players[self.__current_player]
        # 在penalty box中 且 出不來
        if self.__penalty_box.is_player_in_box(current_player):
            self.__next_player()


        print("Answer was correct!!!!")
        self.__players[self.__current_player].set_purse()


        print(self.__players[self.__current_player].get_player_name(),'now has ',
              str(self.__players[self.__current_player].get_purse_status()),
              'Gold Coins.')

        self.__next_player()

        winner = self.__did_player_win()

        return winner



    def wrong_answer(self):
        current_player = self.__players[self.__current_player]
        print("Question was incorrectly answered")
        print(current_player.get_player_name(),"was sent to the penalty box")

        self.__penalty_box.set_player_to_box(current_player)

        self.__next_player()

        winner = self.__did_player_win()

        return winner



    def __next_player(self):
        self.__current_player +=1
        if self.__current_player == len(self.__players):
            self.__current_player = 0


    def __did_player_win(self):
        for player in self.__players:
            if player.get_purse_status() == 6:
                print(player.get_player_name(), "is winner !")
                print("the player's coin is ",player.get_purse_status())
                return True
        return False





class Question:
    def __init__(self,index,category):
        self.__index = index
        self.__category = category
        pass
    def get_index(self):
        return self.__index

    def get_category(self):
        return self.__category




class Player:
    def __init__(self,name):
        self.__name = name
        self.__place = Place()
        self.__purse = Purse()

    def get_player_name(self):
        return self.__name

    def set_place(self,num):
        self.__place.change_place(num)

    def get_place(self):
        return self.__place.get_current_place()

    def set_purse(self):
        self.__purse.add_num_of_coin()

    def get_purse_status(self):
        return self.__purse.get_num_of_coin()





class Penalty_box:
    def __init__(self):
        self.__Box = []

    def is_player_in_box(self,player):
        for i in range(len(self.__Box)):
            if(player == self.__Box[i]):
                return True
        return False

    def set_player_to_box(self,player):
        self.__Box.append(player)

    def set_player_out_box(self,player):
        self.__Box.remove(player)


class Purse:
    def __init__(self):
        self.num_of_coin = 0

    def get_num_of_coin(self):
        return self.num_of_coin

    def add_num_of_coin(self):
        self.num_of_coin+=1

class Place:
    def __init__(self):
        self.__place = 0

    def change_place(self,num):
        self.__place += num
        if self.__place > 11:
            self.__place = self.__place -12

    def get_current_place(self):
        return self.__place



if __name__ == "__main__":
    not_a_winner = False
    game = Game()
    game.set_num_of_questions(50)
    game.set_questions_category('Pop','Science','Sports','Rock')
    player1 = Player("Chet")
    player2 = Player("Pat")
    player3 = Player("Sue")

    game.add(player1)
    game.add(player2)
    game.add(player3)
    game.list_all_players()

    game.start_game()


    while True:

        i = randrange(5)+1

        game.roll(i)
        j = randrange(9)

        if j == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()



        if not_a_winner:break
