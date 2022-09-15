from rest_framework import serializers
from top_scores.models import User, Game, Score

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'email', 'username')


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('name','player_type','genere','game_mode')


class ScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    game = GameSerializer()
    class Meta:
        model = Score
        fields = ('user','score','game')