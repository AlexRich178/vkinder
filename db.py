import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import INTEGER

Base = declarative_base()
engine = sq.create_engine('postgresql://username:password@localhost:5432/dbname')
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()


class BotUsers(Base):
    __tablename__ = 'BotUsers'

    vk_user_id = sq.Column('vk_user_id', sq.Integer, primary_key=True)
    first_name = sq.Column('first_name', sq.String, nullable=False)
    last_name = sq.Column('last_name', sq.String, nullable=False)
    city_id = sq.Column('city_id', sq.Integer)
    last_msg_id = sq.Column('last_msg_id', sq.Integer)
    position = sq.Column('position', sq.Integer)


class SearchingParams(Base):
    __tablename__ = 'SearchingParams'

    search_params_user_id = sq.Column('search_params_user_id', sq.Integer, sq.ForeignKey('BotUsers.vk_user_id'),
                                      primary_key=True)
    search_data_sex = sq.Column('search_data_sex', sq.Integer)
    search_data_age_from = sq.Column('search_data_age_from', sq.Integer)
    search_data_age_to = sq.Column('search_data_age_to', sq.Integer)


class OpenSearchData(Base):
    __tablename__ = 'OpenSearchData'

    search_user_id = sq.Column('search_user_id', INTEGER(unsigned=True), index=True, primary_key=True)
    search_data_user_id = sq.Column('search_data_user_id', sq.Integer, sq.ForeignKey('BotUsers.vk_user_id'))


class Favorites(Base):
    __tablename__ = 'Favorites'

    person_id = sq.Column('person_id', sq.Integer, nullable=False, primary_key=True)
    vk_user_id = sq.Column('vk_user_id', sq.Integer, sq.ForeignKey('BotUsers.vk_user_id'))
    first_name = sq.Column('first_name', sq.String, nullable=False)
    last_name = sq.Column('last_name', sq.String, nullable=False)
    link = sq.Column('link', sq.String, nullable=False)


Base.metadata.create_all(engine)
