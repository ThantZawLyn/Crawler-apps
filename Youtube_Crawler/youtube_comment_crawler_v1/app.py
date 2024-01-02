#imports here
from selenium import webdriver
from googleapiclient.discovery import build
import googleapiclient.errors
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import wget
from random import randint
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import VARCHAR, Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import BYTEA, ENUM
from sqlalchemy.orm import relationship
from sqlalchemy import update
import nltk
import pandas as pd
import re
from sqlalchemy import func, delete
from dateutil import parser
import isodate


Base = declarative_base()

class Yt(Base):
    __tablename__ = 'youtube_channel'
    id = Column(Integer, primary_key=True)
    channel_id = Column("channel_id", VARCHAR(32))
    channel_name = Column("channel_name", VARCHAR(32))
    playlist_id= Column("playlist_id", VARCHAR(32))
    active= Column("active", VARCHAR(32))
    youtube_st = relationship("Yt_st", back_populates="youtube_ch")
    youtube_vdo = relationship("Yt_vd", back_populates="youtube_vdo")

class Yt_st(Base):
    __tablename__ = 'youtube_st'
    id = Column(Integer, primary_key=True)
    subscribers= Column("subscribers", Integer)
    views= Column("views", Integer)
    videos= Column("videos", Integer)
    date= Column('date', DateTime)
    youtube_channel_id = Column(Integer, ForeignKey('youtube_channel.id'))
    youtube_ch = relationship("Yt", back_populates="youtube_st")

class Yt_vd(Base):
    __tablename__ = 'youtube_vd'
    id = Column(Integer, primary_key=True)
    video_id = Column("video_id",  VARCHAR(32))
    youtube_channel_id = Column(Integer, ForeignKey('youtube_channel.id'))
    youtube_vdo = relationship("Yt", back_populates="youtube_vdo")
    nlp_id = Column(Integer, ForeignKey('nlp.id'), nullable=True)
    title =Column("title",  VARCHAR(1024))
    description = Column("description",  VARCHAR(16348))
    tags = Column("tags",  VARCHAR(1024))
    publishedat = Column('publishedat', DateTime)
    viewcount = Column("viewcount", Integer)
    likecount = Column("likecount", Integer)
    commentcount = Column("commentcount", Integer)
    definition = Column("definition",  VARCHAR(32))
    caption = Column("caption",  VARCHAR(32))
    durationsecs = Column("durationsecs", Integer)
    tagcount = Column("tagcount", Integer)
    check = Column('ht_check', VARCHAR(32))
    #nlps = relationship("NLP", back_populates="youtube_vd", uselist=False)
    ht_text = relationship("Yt_httext", back_populates="youtube_vd")


class Yt_cm(Base):
    __tablename__ = 'youtube_comment'
    id = Column(Integer, primary_key=True)
    youtube_vd_id = Column("youtube_vd_id",  VARCHAR(32))
    video_id = Column("video_id",  VARCHAR(32))
    author = Column ("author", VARCHAR(1024))
    authorchannel_url = Column ("authorchannel_url", VARCHAR(1024))
    comment_id = Column ("comment_id", VARCHAR(64))
    #authorchannel_id = Column ("authorchannel_id", VARCHAR(32))
    published_at = Column('published_at', DateTime)
    like_count = Column("like_count", Integer)
    text = Column ("text", VARCHAR(16348))

class Yt_cmlastid(Base):
    __tablename__ = 'yt_cmlastid'
    id = Column(Integer, primary_key=True)
    last_id = Column("last_id", Integer)

class All_comment(Base):
    __tablename__ = 'all_comment'
    id = Column(Integer, primary_key=True)
    comment_id = Column("comment_id", Integer)
    network_id = Column("network_id", Integer)
    nlp_id = Column('nlp_id', Integer)
    
# class NLP(Base):
#     __tablename__ = 'nlp'
#     id = Column('id', Integer, primary_key=True)
#     Category = Column('category', VARCHAR(255))
    
class Yt_ht(Base):
    __tablename__ = 'yt_ht'
    id = Column('id', Integer, primary_key=True)
    hashtag_name = Column('hashtag', VARCHAR(255))
    ht_text = relationship("Yt_httext", back_populates="yt_ht")

class Yt_httext(Base):
    __tablename__ = 'yt_httext'
    id = Column('id', Integer, primary_key=True)
    
    dis_id = Column(Integer, ForeignKey('youtube_vd.id'))
    youtube_vd = relationship("Yt_vd", back_populates="ht_text")

    yt_ht_id = Column(Integer, ForeignKey('yt_ht.id'))
    yt_ht = relationship("Yt_ht", back_populates="ht_text")


engine = create_engine('postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

api_key = 'AIzaSyCR8pd92OA5NgAAz2rjordrmVK5YUYaEv8' # aunng
# api_key = 'AIzaSyCRcHlo9s4XAuqob-GTv7ssfPzefRpcYKM' # ye

api_key = 'AIzaSyAn4uiBw6tcTWbD1d0GRW4QYCT0yMs8qOY'
youtube = build('youtube', 'v3', developerKey= api_key)

def get_comment_details(youtube, video_ids):
    
    comments = []
    # Initialize nextPageToken to None
    next_page_token = None
    # Loop to fetch comments
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId= video_ids,
            maxResults=100,
            pageToken=next_page_token  # Use the nextPageToken
        )
        
        response = request.execute()
        
        for item in response['items']:
            
            comment = item['snippet']['topLevelComment']['snippet']
            comment_id = item['id']  # Extracting comment ID

            comments.append([
                comment_id,  # Adding comment ID
                comment['authorDisplayName'],
                comment['authorChannelUrl'],
                #comment['authorChannelId']['value'],
                comment['publishedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])
        
        # Check if there is a nextPageToken
        next_page_token = response.get('nextPageToken')
        
        if not next_page_token:
            break
    # Create a DataFrame
    return pd.DataFrame(comments, columns=['comment_id','author', 'authorchannel_url', 'published_at', 'like_count', 'text'])
#num_videos = input("Number of videos : ")

video_ids =session.query(Yt_vd.id, Yt_vd.video_id).order_by(Yt_vd.id.desc()).limit(500) 

#video_ids =session.query(Yt_vd.id, Yt_vd.video_id).filter(Yt_vd.id > 198329).order_by(Yt_vd.id.desc()).limit(num_videos) 

for row in video_ids:
    video_ids=row.video_id
    ID = row.id
    print("Youtube Video : " + video_ids)
    print("Youtube Content ID : " +str(ID))
    try:
        comment_df = get_comment_details(youtube,video_ids)
        print("Number of comments : " + str(len(comment_df)))
        if len(comment_df) > 0:
            comment_df['published_at'] = pd.to_datetime(comment_df['published_at'], format='%Y-%m-%d %H:%M:%S')
            comment_df['published_at'] = comment_df['published_at'].dt.tz_convert('Asia/Yangon')
            comment_df['published_at'] = comment_df['published_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
            comment_df['like_count'] = comment_df['like_count'].astype(str)
            comment_df.head(5)
            for i in range(len(comment_df)):
                Comment_id = comment_df['comment_id'].iloc[i]
                Author = comment_df['author'].iloc[i]
                Authorchannel_url = comment_df['authorchannel_url'].iloc[i]
                Published_at = comment_df['published_at'].iloc[i]
                Like_count = comment_df['like_count'].iloc[i]
                Text = comment_df['text'].iloc[i]
                same_id =session.query(Yt_cm.comment_id).filter(Yt_cm.comment_id == Comment_id).first()
                #print(same_id[0])
                if same_id:
                    stmt = (update(Yt_cm).where(Yt_cm.comment_id == same_id[0]).values(like_count=Like_count)) # update views, like, comment
                    session.execute(stmt, execution_options={"synchronize_session": False})
                    session.commit() 
                    #session.rollback()
                    print("Sucessfully updated to DB")
                else:
                    add_vd= Yt_cm(youtube_vd_id=ID, video_id=video_ids, author=Author,authorchannel_url= Authorchannel_url,
                            comment_id =Comment_id, published_at=Published_at, like_count=Like_count, 
                            text = Text) # add youtube_comment
                    session.add(add_vd)
                    session.commit() 
                    #session.rollback()

                    latest_id =session.query(func.max(Yt_cm.id)).first() # add id to all_comment
                    add_id = All_comment(comment_id = latest_id[0], network_id =2)
                    session.add(add_id)
                    session.commit() 
                    update_lastid = (update(Yt_cmlastid).where(Yt_cmlastid.id == 1).values(last_id=ID)) # update last id
                    session.execute(update_lastid, execution_options={"synchronize_session": False})
                    session.commit() 
                    #session.rollback()
            print("Sucessfully Added to DB")
    except Exception as e:
        print("The error is: ", e)
    print("--------------------------------")
    sleep(0.5)
session.commit() 
session.rollback()

