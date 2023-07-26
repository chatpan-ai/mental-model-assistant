# -*- encoding: utf8 -*- 


import databases
import sqlalchemy
import ormar
from typing import Optional


DB_URI = "sqlite:///model.db"

database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()


class MentalModel(ormar.Model):
    class Meta:
        tablename = "mental_model"

        database = database
        metadata = metadata
        
        constraints = [ormar.UniqueColumns("title")]


    id: Optional[int] = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=200)
    summary: str = ormar.Text()
    tags: str = ormar.Text() # comma separated
    chatpan_assistant_uuid: str = ormar.String(max_length=100)
    chatpan_room_uuid: str = ormar.String(max_length=100)


def create_all():
    engine = sqlalchemy.create_engine(DB_URI)
    metadata.create_all(engine)

if __name__ == '__main__':
    create_all()
    
    
