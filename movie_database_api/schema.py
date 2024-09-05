import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Movie as MovieModel, Genre as GenreModel
from models import db_session

class MovieType(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class GenreType(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class Query(graphene.ObjectType):
    get_movies_by_genre = graphene.List(MovieType, genre_id=graphene.ID(required=True))
    get_genre_by_movie = graphene.List(GenreType, movie_id=graphene.ID(required=True))

    def resolve_get_movies_by_genre(self, info, genre_id):
        genre = db_session.query(GenreModel).filter_by(id=genre_id).first()
        if genre:
            return genre.movies
        return []

    def resolve_get_genre_by_movie(self, info, movie_id):
        movie = db_session.query(MovieModel).filter_by(id=movie_id).first()
        if movie:
            return movie.genres
        return []

class CreateGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(GenreType)

    def mutate(self, info, name):
        if not name or len(name) > 100:
            raise Exception("Invalid genre name")
        genre = GenreModel(name=name)
        db_session.add(genre)
        db_session.commit()
        return CreateGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    genre = graphene.Field(GenreType)

    def mutate(self, info, id, name):
        genre = db_session.query(GenreModel).filter_by(id=id).first()
        if not genre:
            raise Exception("Genre not found")
        if not name or len(name) > 100:
            raise Exception("Invalid genre name")
        genre.name = name
        db_session.commit()
        return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        genre = db_session.query(GenreModel).filter_by(id=id).first()
        if not genre:
            raise Exception("Genre not found")
        db_session.delete(genre)
        db_session.commit()
        return DeleteGenre(success=True)

class Mutation(graphene.ObjectType):
    create_genre = CreateGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()
