from django.core.cache import cache
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView

from top_scores.serializers import UserSerializer, GameSerializer, ScoreSerializer
from top_scores.constants import TOP_SCORE_COUNT
from top_scores.models import Score
from top_scores.tasks import add_or_update_score


class AddUserView(generics.CreateAPIView):
    '''
    @payload {
        name:string,
        email:string
    }
    @return: user details
    '''
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class AddGameView(generics.CreateAPIView):
    '''
    ('name','player_type','genere','game_mode')
    @payload {
        name:string,
        player_type:string,
        genere:string,
        game_mode:string
    }
    @return: game details
    '''
    permission_classes = (AllowAny,)
    serializer_class = GameSerializer


class PublishScoreView(APIView):
    '''
    @payload:[
        {
            user_id:int, 
            game_id:int, 
            game_no:int, 
            score:float
        }
    ]
    @param: self
    @param: request
    @return:
    '''
    def post(self, request, *args, **kwargs):
        try:
            payload = request.data
            last_score = cache.get(f'top_{TOP_SCORE_COUNT}_last_score') or 0
            update_top_scores = False

            if type(payload) is not list:
                return Response({'Success':False, 'Message':'Invalid data format'}, status=HTTP_400_BAD_REQUEST)

            scores = []
            for data in payload:

                if data.get('user_id') is not int or data.get('game_id') is not int or data.get('game_no') is not int or data.get('score') is not float:
                    print(f"Invalid data with values {data.get('user_id')} {data.get('game_id')} {data.get('game_no')} {data.get('score')}")
                    continue

                scores.append(Score(user_id=data.get('user_id'), game_id=data.get('game_id'), game_no=data.get('game_no'), score=data.get('score')))
                if not update_top_scores and data.get('score')>last_score:
                    update_top_scores = True
            
            Score.objects.bulk_create(scores)
            if update_top_scores:
                add_or_update_score.delay(TOP_SCORE_COUNT)

            return Response({'Success':True}, status=HTTP_201_CREATED)
        except Exception as e:
            return Response({'Success':False, 'Message':f'{e}'}, status=HTTP_400_BAD_REQUEST)


class GetTopScore(APIView):
    '''
    @payload:{
        count:int
        }
    @param: self
    @param: request
    @return: list
    '''
    def get(self, request, *args, **kwargs):
        count = kwargs.pop('count')

        if not count:
            return Response({'Success':False, 'Message':'Invalid data'}, status=HTTP_400_BAD_REQUEST)

        scorers = cache.get(f'top_{count}_scorers')
        if not scorers:
            add_or_update_score(count)
            scorers = cache.get(f'top_{count}_scorers')

        return Response({'Success':True, 'data':ScoreSerializer(Score.objects.filter(id__in=scorers), many=True).data}, status=HTTP_200_OK)
