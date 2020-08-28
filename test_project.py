#!/usr/bin/python
import argparse
from tinkoff_voicekit_client import ClientSTT
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker
import os


Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    date = Column('date', DateTime)
    id = Column(Integer, primary_key=True)
    action = Column('action', Integer)
    phone = Column('phone', Integer)
    duration = Column('duration', Float)
    result = Column('result', String)


api_key = input(str('Print your api key: '))
secret_key = input(str('Print your secret key: '))
client = ClientSTT(api_key=api_key, secret_key=secret_key)
audio_config = {
    "encoding": 'LINEAR16',
    "sample_rate_hertz": 8000,
    "num_channels": 1
}
# Парсим командную строку
parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store_true')
parser.add_argument('path', type=str)
parser.add_argument('number', type=int)
parser.add_argument('step', type=int, choices=range(1, 3))
args = parser.parse_args()


def main(path, number, step, save=False):
    try:
        # Step 1: получаем аргументы из командной строки и расшифровываем файл
        recognize = client.recognize('{}'.format(path), audio_config)
        duration = float(recognize[0]['end_time'][:-1])
        text = recognize[0]['alternatives'][0]['transcript'].lower()
        # Step 2: соответствующим образом обрабатываем файл
        if step == 1:
            if 'автоответчик' in text:
                action = 0
            else:
                action = 1
        else:
            text = text.split(' ')
            for word in text:
                if word.startswith('не'):
                    action = 0
                    break
                else:
                    action = 1
        # Step 3: если выставлен флаг - сохраняем в postgre
        if save:
            engine = create_engine('postgresql://postgres:your_password@localhost/test_base')
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()
            new_post = Post(date=datetime.now(), action=action, phone=number, duration=duration, result=text)
            session.add(new_post)
            session.commit()
        # Step 4: аналогичным образом сохраняем логи в .txt файл
        to_write = '{}, {}, {}, {}, {}, {}'.format(datetime.now(), int(datetime.now().timestamp()), action, number,
                                                   duration, text) + '\n'
        try:
            with open('logs.txt', mode='x') as file:
                file.write(to_write)
        except FileExistsError:
            with open('logs.txt', mode='a') as file:
                file.write(to_write)
        # Step 5: удаляем .wav файл
        os.remove(path=path)
    except Exception as err:
        print(err)
        to_write = '{}: {}'.format(datetime.now(), err) + '\n'
        try:
            with open('logs_errors.txt', mode='x') as file:
                file.write(to_write)
        except FileExistsError:
            with open('logs_errors.txt', mode='a') as file:
                file.write(to_write)


if __name__ == '__main__':
    main(args.path, args.number, args.step, args.s)
