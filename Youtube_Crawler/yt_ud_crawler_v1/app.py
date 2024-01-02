from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime, timedelta, timezone
import time
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import VARCHAR, Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy import update
from sqlalchemy import func, delete
from sqlalchemy.orm import relationship

Base = declarative_base()

class Yt(Base):
    __tablename__ = 'youtube_channel'
    id = Column(Integer, primary_key=True)
    channel_id = Column("channel_id", VARCHAR(32))
    channel_name = Column("channel_name", VARCHAR(32))
    playlist_id= Column("playlist_id", VARCHAR(32))
    youtube_st = relationship("Yt_st", back_populates="youtube_ch")
    youtube_ud = relationship("Yt_ud", back_populates="youtube_ud")

class Yt_st(Base):
    __tablename__ = 'youtube_st'
    id = Column(Integer, primary_key=True)
    subscribers= Column("subscribers", Integer)
    views= Column("views", Integer)
    videos= Column("videos", Integer)
    date= Column('date', DateTime)
    youtube_channel_id = Column(Integer, ForeignKey('youtube_channel.id'))
    youtube_ch = relationship("Yt", back_populates="youtube_st")

class Yt_ud(Base):
    __tablename__ = 'youtube_ud'
    id = Column(Integer, primary_key=True)
    subscribers= Column("subscribers", Integer)
    views= Column("views", Integer)
    videos= Column("videos", Integer)
    date= Column('date', DateTime)
    youtube_channel_id = Column(Integer, ForeignKey('youtube_channel.id'))
    youtube_ud = relationship("Yt", back_populates="youtube_ud")
    
engine = create_engine('postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs', echo=False)
#Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


api_key = 'AIzaSyCRcHlo9s4XAuqob-GTv7ssfPzefRpcYKM'
#channel_id = 'UCjO7yctWXGCeTFqQSV_2smw'
channel_ids = [ 'UCjO7yctWXGCeTFqQSV_2smw', # cni
                'UC8ISzz4zf1arThg-JYD9E3w', # popular
                'UCBwkuaC-tV3ppkg09yPRwyQ', # ymg
                'UCeldBKnJ5eSNaJ4IMo97K-Q', # 8day
                'UC1P3hSh0VsVEjTki3eaue5Q', # mtnews
                'UCTO6VAbStROisLZBYw0diVQ', # myanmar celebrity
                'UCzoPb9sKVAHd-pIzv9RGGRA', # eleven
                'UCRUnmIWu89R1KrLJ_khcOHw', # vidya
                'UCcAc8z94v9HOF63PPQzWL6Q', # Myanmar Media 7 Entertainment
                'UC8gCDg2aAaC2Sz6ti2XI6xg', # the standard time daily
                'UCTjrvGXmOIXns8mXz3-LrJg', # Myanmar platform  
                'UCtqwk50GLaaxir6k4WJefPg', # 36 myanmar
                'UCnl3Ao-BMDYvF1kTIDey60Q', # Western News
                'UCPxUXfbroDTTs1SO2K5GOtQ', # Pyi Myanmar
                'UCBcrr0H5Q5l0cdcWQPiZ4tg', # Delta News Agency
                'UCigcOsgmm9Xw0bHlHW86kEQ', # One News Myanmar
                'UCd9maKo3B6jX8pCPzLa2hvA', # BBC မြန်မာ
                'UCv-YbGueeYCp8_CdjgXQD3A', # VOA Burmese
                'UCJEaYn-fXd6FdQknoAaL5ag', # Tachileik News Agency
                'UCKHarniWYDtOHhtiG6T48RA', # MeKong News
                'UCJpykv7SLazaVzdurxhURIg', # Myaelatt Athan
                'UCFsA1mMDxssJOow7WG686SA', # BETV Business
                'UCuLbje_7glVUKWNjSQEpu4w', # Ayeyarwaddy Times
                'UCP2LE30cd1D0yAsfoOOsC6Q', # Shwe Phee Myay News
                'UCYcM3RJV34iqUbX3Fau-hZQ', # Thanlwin Khet News
                'UCXHQbAtQhv1y5nVS3bZzbsg', # News Watch Journal
                'UCcxwEY-jPcidUTeWLqaH5MA', # Myanmar Witness
                'UCzZNXzUgaT2pWRLZTIncGeQ', # Development Media Group
                'UCclbf3n8sEZTpKm4tJw93wA', # Red News Agency
                'UCE75dgnEYPacknHHg3a3sJg', # RFA Burmese
                'UCgVG_9h2FI2D4Z1d_z4t3Hg', # Narinjara
                'UCKud809KUMIyNhqwuy5JeFw', # Myanmar Now
                'UCuaRmKJLYaVMDHrnjhWUcHw', # DVB TV News
                'UCktBWlYbAf4en-pWyyTqRwg', # khit thit media
                'UCk9f0cLiMmtchQySOogzoig', # Mizzima - News in Burmese
                'UCvEeefnYBBY1HaxG7JYo1bw',  # SKY NET DTH
                'UCescNYA72EeuJYEU555d7_g',   # Cele Gabar
                'UCclbf3n8sEZTpKm4tJw93wA', # Red news agency
                'UCo0U2Mpumt3gTeBDpP28ZrA', # Sunday Journal
                'UCZFDThZ7CuFqXLn3Zb4bt7g'  # 8 days entertainment
                ]
youtube = build('youtube', 'v3', developerKey= api_key)

date = datetime.now()
date_format = "%Y-%m-%d %H:%M:%S"
date= datetime.strftime(date, date_format)
#print(date)
def get_channel_stats(youtube,channel_ids):
    all_data =[]
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(Channel_id=response['items'][i]['id'],
                    Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers =response['items'][i]['statistics']['subscriberCount'],
                    Views =response['items'][i]['statistics']['viewCount'],
                    Videos =response['items'][i]['statistics']['videoCount'],
                    Playlist_id =response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                    Date = date
                    )
        all_data.append(data)
    return all_data

channel_statistics=get_channel_stats(youtube, channel_ids)
channel_data=pd.DataFrame(channel_statistics)
print("Total Channel : " + str(len(channel_data)))

for i in range(len(channel_data)):
    Channel_id = channel_data['Channel_id'].iloc[i]
    Channel_name=channel_data['Channel_name'].iloc[i]
    Subscribers=channel_data['Subscribers'].iloc[i]
    Views= channel_data['Views'].iloc[i]
    Videos= channel_data['Videos'].iloc[i]
    Playlist_id= channel_data['Playlist_id'].iloc[i]
    Date = channel_data['Date'].iloc[i]
    same_id =session.query(Yt.id).filter(Yt.channel_id == Channel_id).first() # check id exit in db
    #print(same_id[0])
    if same_id:
        stmt = (update(Yt_ud).where(Yt_ud.youtube_channel_id == same_id[0]).values(subscribers=Subscribers, views=Views, videos=Videos, date=Date)) # update views, like, comment
        session.execute(stmt, execution_options={"synchronize_session": False})
        session.commit() 
        session.rollback()
print("Sucessfully Added to DB")