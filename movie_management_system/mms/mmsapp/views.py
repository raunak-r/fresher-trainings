from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.db.models import Subquery
from rest_framework import serializers
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from .models import User, Movie, Genre, Review, MovieCast, MovieDirector, Watchlist
from .serializers import UserSerializer, MovieSerializer, MovienSerializer, GenreSerializer, ReviewSerializer, \
    MovieCastSerializer, MovieDirectorSerializer, WatchlistSerializer

# Create your views here.


def home_page(request):

    return render(request, 'mmsapp/home.html', {'title':'Home'})


# @api_view(['GET', 'POST','PUT','PATCH','DELETE'])
# @csrf_exempt
# def user_list(request,user_id=None,format=None):
#     if request.method == 'GET':
#         if user_id is not None:
#             #retreive only that user
#             user_obj= User.objects.filter(user_id=user_id)
#             serializer = UserSerializer(user_obj, many=True)
#             return JsonResponse({'user':serializer.data})
#         else:
#             users = User.objects.all()
#             serializer = UserSerializer(users, many=True)
#             return JsonResponse({'users': serializer.data})

#     elif request.method == 'POST':
#         try:
#             jsonData = JSONParser().parse(request)
#             serializer = UserSerializer(data=jsonData)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#             else:
#                 return JsonResponse(serializer.errors, safe=False)

#         except json.JSONDecodeError as e:
#             # Handle the JSONDecodeError exception
#             return HttpResponseBadRequest('Invalid JSON payload: {}'.format(e.msg))
#         except Exception as e:
#             # Handle other exceptions
#             return HttpResponseBadRequest('Error while parsing JSON payload: {}'.format(str(e)))
#         # Return a success response
#         # return HttpResponse('Success!')
#     elif request.method == 'PUT':
#         try:
#             jsonData = JSONParser().parse(request)
#             user = User.objects.get(user_id=user_id)
#             serializer = UserSerializer(user, data=jsonData)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except json.JSONDecodeError as e:
#             return HttpResponseBadRequest('Invalid JSON payload: {}'.format(e.msg))
#         except Exception as e:
#             return HttpResponseBadRequest('Error while parsing JSON payload: {}'.format(str(e)))
#     elif request.method == 'PATCH':
#         try:
#             jsonData = JSONParser().parse(request)
#             user = User.objects.get(user_id=user_id)
#             serializer = UserSerializer(user, data=jsonData,partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return JsonResponse(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except json.JSONDecodeError as e:
#             return HttpResponseBadRequest('Invalid JSON payload: {}'.format(e.msg))
#         except Exception as e:
#             return HttpResponseBadRequest('Error while parsing JSON payload: {}'.format(str(e)))
#     elif request.method == 'DELETE':
#         user = User.objects.get(user_id=user_id)
#         user.delete()
#         return JsonResponse({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        context = {
            'users': serializer.data
        }
        return render(request, 'mmsapp/user.html', context)

    def post(self, request, format=None):
        # jsonData = JSONParser().parse(request)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, safe=False)


class UserDetails(APIView):

    def get(self,request,user_id=None, format=None):
        if user_id is not None:
            user_obj = User.objects.filter(user_id=user_id)
            if user_obj.exists():
                serializer = UserSerializer(user_obj, many=True)
                return JsonResponse({'user': serializer.data})
            else:
                return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return JsonResponse({'users': serializer.data})

    def put(self,request,user_id=None, format=None):
        # jsonData = JSONParser().parse(request)
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,user_id=None, format=None):
        # jsonData = JSONParser().parse(request)
        user = User.objects.get(user_id=user_id)
        serializer = UserSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,user_id=None,format=None):
        user = User.objects.get(user_id=user_id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
                   

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
      # return JsonResponse({'movies': serializer.data})
    context = {
        'movies' : serializer.data
    }
    return render(request,'mmsapp/movie.html',context)

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return JsonResponse({'genres': serializer.data})


@api_view(['GET'])
def moviegenre_list(request, genre, format=None):
    try:
        genre_obj = Genre.objects.get(genre_type=genre)
        movies = Movie.objects.filter(genre_id=genre_obj)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except  Genre.DoesNotExist:
        return Response(f"No movies found for genre '{genre}'", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def directormovie_list(request, director, format=None):
    try:
        genre_obj = Genre.objects.get(genre_type=director)
        movies = Movie.objects.filter(genre_id=genre_obj)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    except  Genre.DoesNotExist:
        return Response(f"No movies found for genre '{director}'", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def moviename_list(request, partial_name, format=None):
    try:
        movies = Movie.objects.filter(movie_name__icontains=partial_name)
        if movies.exists():
            serialized_movies = MovieSerializer(movies, many=True)
            return Response(serialized_movies.data, status=status.HTTP_200_OK)
        else:
            return Response(f"No movies found for partialname '{partial_name}'", status=status.HTTP_404_NOT_FOUND)

    except Movie.DoesNotExist:
        return Response(f"No movies found for partialname '{partial_name}'", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_movie_by_director(request, director, format=None):
    # Query the movies based on director name
    movies = Movie.objects.filter(director__icontains=director)
    if movies.exists():
        movie_titles = [movie.title for movie in movies]
        return JsonResponse({'movies': movie_titles})
    else:
        return JsonResponse({'message': f"No movies found for director '{director}'"}, status=404)


@api_view(['GET'])
def get_movie_by_director(request, director, format=None):
    try:
        director_obj = User.objects.get(user_name=director)
        movie_ids = Moviedirector.objects.filter(director_id=director_obj.user_id).values('movie_id').distinct()
        movies = Movie.objects.filter(movie_id__in=Subquery(movie_ids)).values('movie_name')
        serializer = MovienSerializer(movies, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return JsonResponse({'error': f'director {director} does not exist'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
