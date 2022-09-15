import json
from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APITestCase


from top_scores.models import User, Game, Score
from top_scores.serializers import ScoreSerializer


class UserModelCases(TestCase):

    def setUp(self):
        pass


    def add_user(self, name:str, email:str) -> User:
        return User.objects.create(name=name,email=email)


    def test_email_uniqueness(self) -> None:
        try:
            self.add_user(name='Shaishav', email='Shaishav@email.com')
            self.add_user(name='Dhruv', email='Shaishav@email.com')
            self.fail("Failed Unique Email Check for User with data name shair email Shaishav@email.com")
        except IntegrityError:
            pass
        except Exception as e:
            print(f'Exception {e} raised in UserModelTest.test_email_uniqueness')


    def test_username_creation(self) -> None:
        user = self.add_user(name='Shaishav',email='Shaishav@email.com')
        self.assertEqual(user.username, "Shaishav")


class GetTopScoreCases(APITestCase):

    def add_user(self, name:str, email:str) -> User:
        return User.objects.create(name=name,email=email)

    def add_score(self, user_id:int, game_id:int, score:int, game_no:int) -> Score:
        return Score.objects.create(user_id=user_id, game_id=game_id, score=score, game_no=game_no)

    def setUp(self) -> None:
        first_game = 1
        second_game = 2

        #User
        suresh = self.add_user(name="Suresh",email="Suresh@email.com")
        ramesh = self.add_user(name="Ramesh",email="Ramesh@email.com")
        brijesh = self.add_user(name="Brijesh",email="Brijesh@email.com")
        rajesh = self.add_user(name="Rajesh",email="Rajesh@email.com")
        mahesh = self.add_user(name="Mahesh",email="Mahesh@email.com")
        ekesh = self.add_user(name="Ekesh",email="Ekesh@email.com")

        #Game
        game = Game.objects.create(name='Pubg', player_type=Game.MULTIPLAYER, genere=Game.COMPETETIVE, game_mode=Game.ONLINE)

        #Score
        self.add_score(user_id=suresh.id, game_id=game.id, score=20, game_no=first_game)
        self.add_score(user_id=ramesh.id, game_id=game.id, score=10, game_no=first_game)
        self.add_score(user_id=brijesh.id, game_id=game.id, score=30, game_no=first_game)
        self.add_score(user_id=rajesh.id, game_id=game.id, score=40, game_no=second_game)
        self.add_score(user_id=mahesh.id, game_id=game.id, score=60, game_no=second_game)
        self.add_score(user_id=ekesh.id, game_id=game.id, score=50, game_no=second_game)
        self.add_score(user_id=suresh.id, game_id=game.id, score=60, game_no=second_game)
    
    def are_they_equal(self, actual:list, expected:list) -> bool:
        try:
            if type(expected) is not list or type(actual) is not list or len(expected)!=len(actual):
                return "data type not matching"
            
            freq = {}

            for data in actual:
                if not freq.get(data.get('user').get('email')):
                    freq[data.get('user').get('email')] = 0
                if not freq.get(data.get('score')):
                    freq[data.get('score')] = 0
                
                freq[data.get('user').get('email')] += 1
                freq[data.get('score')] += 1

            for data in expected:

                freq[data.get('user').get('email')] -= 1
                if freq[data.get('user').get('email')] == 0:
                    del freq[data.get('user').get('email')]
                

                freq[data.get('score')] -= 1
                if freq[data.get('score')] == 0:
                    del freq[data.get('score')]

            return None if len(freq)==0 else "frequency different"

        except Exception as e:
            return e.message()

    def top_score_for_count(self, count:int) -> None:
        _resp = self.client.get(f'/top_scores/get_top_score/{count}', {}, True)
        _response = _resp.json().get('data')
        _expected_response = json.loads(json.dumps(ScoreSerializer(Score.objects.all().order_by('-score')[:count], many=True).data))
        
        message = self.are_they_equal(_response, _expected_response) 
        if message:
            self.fail(message)

    def test_top_score(self):
        self.top_score_for_count(1)
        self.top_score_for_count(2)
        self.top_score_for_count(5)
