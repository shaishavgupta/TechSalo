from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeStampModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, db_index=True, null=False, blank=False, unique=True)
    username = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        self.username = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'

    def __unicode__(self):
        return f'{self.id} - {self.name}'


class Game(TimeStampModel):
    MULTIPLAYER = 'multi_player'
    SINGLEPLAYER = 'single_player'

    OFFLINE = 'offline'
    ONLINE  = 'online'

    SPORTS = 'sports'
    RPG = 'rpg'
    COMPETETIVE = 'competetive'
    OTHERS = 'others'

    GENERE = {
        (SPORTS, SPORTS),
        (RPG, RPG),
        (COMPETETIVE, COMPETETIVE),
        (OTHERS, OTHERS),
    }

    PLAYER_TYPE = {
        (MULTIPLAYER, MULTIPLAYER),
        (SINGLEPLAYER, SINGLEPLAYER)
    }

    GAME_MODE = {
        (OFFLINE, OFFLINE),
        (ONLINE, ONLINE)
    }

    name = models.CharField(max_length=100, null=False, blank=False)
    player_type = models.CharField(choices=PLAYER_TYPE, max_length=100, null=False, blank=False)
    genere = models.CharField(choices=GENERE, max_length=100, null=False, blank=False)
    game_mode = models.CharField(choices=GAME_MODE, max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'games'
        unique_together = ('name', 'game_mode')

    def __unicode__(self):
        return f'{self.id} - {self.name}'


class Score(TimeStampModel):
    user = models.ForeignKey(User, related_name="user_score", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, related_name="game_score", on_delete=models.CASCADE)
    score = models.FloatField()
    game_no = models.IntegerField()

    class Meta:
        db_table = 'scores'
        unique_together = ('user', 'game_no')
    
    def __unicode__(self):
        return f'{self.id} - {self.user.name} - {self.game.name} - {self.score}'