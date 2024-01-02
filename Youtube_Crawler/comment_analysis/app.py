import enum
from sqlalchemy import VARCHAR, Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import BYTEA, ENUM
from sqlalchemy.orm import relationship
# from ..database import Base
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pyidaungsu as pds
import os
import sqlalchemy as db
import base64
import re
from keras.models import load_model
import emoji
#imports here
from selenium import webdriver
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
import os
from googletrans import Translator
translator = Translator()


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # hide warning
# from ..constants import SQLALCHEMY_DATABASE_URI

#engine = create_engine(SQLALCHEMY_DATABASE_URI)
engine = create_engine('postgresql://fbs:yah7WUy1Oi8G@172.32.253.129:5432/fbs', echo=False)

Base = declarative_base(bind=engine)
session_creator = sessionmaker()
DBSession = session_creator()

class LikeType(enum.Enum):
    like = "like"
    love = "love"
    haha = "haha"
    wow = "wow"
    sad = "sad"
    angry = "angry"

class TaskType(str, enum.Enum):
    keyword: str = "keyword"
    source: str = "source"
    like: str = "like"
    comment: str = "comment"
    share: str = "share"
    personal_page: str = "personal_page"

class SubtaskType(str, enum.Enum):
    like: str = "like"
    comment: str = "comment"
    share: str = "share"
    personal_page: str = "personal_page"

class TaskStatus(str, enum.Enum):
    in_queue: str = "in_queue"
    in_progress: str = "in_progress"
    success: str = "success"
    retry: str = "retry"
    failed: str = "failed"

class Subtask(Base):
    __tablename__ = 'subtasks'
    id = Column('id', Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="subtasks", uselist=False)

    subtask_type = Column(ENUM(SubtaskType))

    start_time = Column('start_time', DateTime)
    end_time = Column('end_time', DateTime)

    status = Column(ENUM(TaskStatus))

class SubtaskPersonalData(Base):
    __tablename__ = 'subtask_personal_data'
    id = Column('id', Integer, primary_key=True)
    subtask_id = Column(Integer, ForeignKey('subtasks.id'))
    subtask = relationship("Subtask")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

class Post(Base):
    __tablename__ = 'posts'

    def __hash__(self):
        return hash(self.fb_post_id)

    def __eq__(self, other):
        return isinstance(other, Post) and self.fb_post_id == other.fb_post_id

    id = Column('id', Integer, primary_key=True)
    date = Column('date', DateTime)
    last_time_updated = Column('last_time_updated', DateTime)
    fb_post_id = Column('fb_post_id', VARCHAR(1024))
    fb_repost_id = Column('fb_repost_id', VARCHAR(128))
    fb_repost_link = Column('fb_repost_link', VARCHAR(2048))
    fb_post_link = Column('fb_post_link', VARCHAR(1024))
    fb_post_link_likes = Column('fb_post_link_likes', VARCHAR(1024))
    content_id = Column(Integer, ForeignKey('content.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    stat_id = Column(Integer, ForeignKey('post_stat.id'))

    content = relationship("Content", back_populates="post", uselist=False)
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")
    shares = relationship("Share", back_populates="post")
    user = relationship("User", back_populates="post", uselist=False)
    task = relationship("Task", back_populates="post", uselist=False)
    stat = relationship("PostStat", back_populates="post", uselist=False)
    subtasks = relationship("Subtask", back_populates="post", uselist=True)

class PostStat(Base):
    __tablename__ = 'post_stat'
    id = Column('id', Integer, primary_key=True)
    likes = Column('likes', VARCHAR(32))
    comments = Column('comments', VARCHAR(32))
    shares = Column('shares', VARCHAR(32))

    post = relationship("Post", back_populates="stat", uselist=False)

    def is_equals(self, post_stat):
        return self.likes == post_stat.likes and self.comments == post_stat.comments and self.shares == post_stat.shares

class Content(Base):
    __tablename__ = 'content'
    id = Column('id', Integer, primary_key=True)
    text = Column('text', VARCHAR(1024))
    nlp_id = Column(Integer, ForeignKey('nlp.id'),  nullable=True)

    post = relationship("Post", back_populates="content", uselist=False)
    comment = relationship("Comment", back_populates="content", uselist=False)
    photos = relationship("Photo", back_populates="content", uselist=True)
    videos = relationship("Video", back_populates="content", uselist=True)

class NLP(Base):
    __tablename__ = 'nlp'
    id = Column('id', Integer, primary_key=True)
    Category = Column('category', VARCHAR(255))
    
class Photo(Base):
    __tablename__ = 'photos'
    id = Column('id', Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey('content.id'))
    photo_link = Column('photo_link', VARCHAR(1024))

    content = relationship("Content", back_populates="photos")

class Video(Base):
    __tablename__ = 'videos'
    id = Column('id', Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey('content.id'))
    video_link = Column('video_link', VARCHAR(1024))

    content = relationship("Content", back_populates="videos")

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True)

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="likes")

    comment_id = Column(Integer, ForeignKey('comments.id'))
    comment = relationship("Comment", back_populates="likes")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="likes")

    like_type = Column(ENUM(LikeType))

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)

    date = Column(DateTime)
    fb_comment_id = Column('fb_comment_id', VARCHAR(255))

    content_id = Column(Integer, ForeignKey('content.id'))
    content = relationship("Content", back_populates="comment")

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="comments")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="comments")

    parent_comment_id = Column(Integer, ForeignKey('comments.id'))
    parent_comment = relationship("Comment", back_populates="child_comments", remote_side=[id])
    child_comments = relationship("Comment", back_populates="parent_comment", remote_side=[parent_comment_id])

    likes = relationship("Like", back_populates="comment")
    likes_count = Column('likes_count', Integer)

class Share(Base):
    __tablename__ = 'shares'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="shares")

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="shares")

class UserUniversity(Base):
    __tablename__ = 'user_university'
    id = Column(Integer, primary_key=True)
    name = Column('name', VARCHAR(1024))
    info = Column('info', VARCHAR(1024))
    link = Column('link', VARCHAR(1024))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="universities")

class UserJob(Base):
    __tablename__ = 'user_job'
    id = Column(Integer, primary_key=True)
    name = Column('name', VARCHAR(1024))
    info = Column('info', VARCHAR(1024))
    link = Column('link', VARCHAR(1024))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="jobs")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)

    name = Column("name", VARCHAR(1024))
    link = Column("link", VARCHAR(1024))
    sex = Column("sex", VARCHAR(8))
    city_of_birth = Column("city_of_birth", VARCHAR(128))
    current_city = Column("current_city", VARCHAR(128))
    birthday = Column("birthday", VARCHAR(128))
    fb_id = Column("fb_id", VARCHAR(32))
    check = Column("check",Boolean)
    
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    shares = relationship("Share", back_populates="user")
    post = relationship("Post", back_populates="user")

    universities = relationship("UserUniversity", back_populates="user")
    jobs = relationship("UserJob", back_populates="user")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column('id', Integer, primary_key=True)
    interval = Column('interval', Integer)
    retro = Column('retro', DateTime)
    until = Column('until', DateTime)
    received_time = Column('received_time', DateTime)
    finish_time = Column('finish_time', DateTime)
    status = Column(ENUM(TaskStatus))
    enabled = Column('enabled', Boolean)
    post = relationship("Post", back_populates="task")

class TaskKeyword(Base):
    __tablename__ = 'tasks_keyword'
    id = Column('id', Integer, primary_key=True)
    keyword = Column('keyword', VARCHAR(255))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task")

class TaskSource(Base):
    __tablename__ = 'tasks_source'
    id = Column('id', Integer, primary_key=True)
    source_id = Column('source_id', VARCHAR(255))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task")

class WorkerCredential(Base):
    __tablename__ = 'worker_credentials'
    id = Column('id', Integer, primary_key=True)
    inProgress = Column('inProgress', Boolean)
    inProgressTimeStamp = Column('in_progress_timestamp', DateTime)
    last_time_finished = Column('last_time_finished', DateTime)
    locked = Column('locked', Boolean)
    alive_timestamp = Column('alive_timestamp', DateTime)

    account_id = Column(Integer, ForeignKey('accounts.id'))
    proxy_id = Column('proxy_id', ForeignKey('proxy.id'))
    user_agent_id = Column('user_agent_id', ForeignKey('user_agent.id'))

    account = relationship("FBAccount", uselist=False)
    proxy = relationship("Proxy", uselist=False)
    user_agent = relationship("UserAgent", uselist=False)

class WorkingCredentialsTasks(Base):
    __tablename__ = 'worker_credentials_tasks'
    id = Column('id', Integer, primary_key=True)
    worker_credentials_id = Column(Integer, ForeignKey('worker_credentials.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    type = Column('type', VARCHAR(16))
    start_timestamp = Column('start_timestamp', DateTime)
    finish_timestamp = Column('finish_timestamp', DateTime)

class Proxy(Base):
    __tablename__ = 'proxy'
    id = Column('id', Integer, primary_key=True)
    host = Column('host', VARCHAR(255))
    port = Column('port', Integer)
    login = Column('login', VARCHAR(255))
    password = Column('password', VARCHAR(255))
    available = Column('available', Boolean)
    last_time_checked = Column('last_time_checked', DateTime)
    attempts = Column('attempts', Integer)

class FBAccount(Base):
    __tablename__ = 'accounts'
    id = Column('id', Integer, primary_key=True)
    login = Column('login', VARCHAR(255))
    password = Column('password', VARCHAR(255))
    available = Column('available', Boolean, nullable=False)
    cookies = relationship("Cookies", uselist=False)
    availability_check = Column('availability_check', DateTime)

class Cookies(Base):
    __tablename__ = 'cookies'
    id = Column('id', Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    row_data = Column('row_data', BYTEA)

class UserAgent(Base):
    __tablename__ = 'user_agent'
    id = Column('id', Integer, primary_key=True)
    userAgentData = Column('userAgentData', VARCHAR(2048))
    window_size_id = Column(Integer, ForeignKey('window_size.id'))
    window_size = relationship("WindowSize")

class WindowSize(Base):
    __tablename__ = 'window_size'
    id = Column('id', Integer, primary_key=True)
    width = Column('width', Integer)
    height = Column('height', Integer)



class All_content(Base):
    __tablename__ = 'all_content'
    id = Column(Integer, primary_key=True)
    content_id = Column("content_id", Integer)
    network_id = Column("network_id", Integer)
    nlp_id = Column('nlp_id', Integer)
    ht_check = Column('ht_check', VARCHAR(32))
    keyword_check = Column('keyword_check', VARCHAR(32))

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

class Tg(Base):
    __tablename__ = 'tele_content'
    id = Column(Integer, primary_key=True)
    username = Column("username", VARCHAR(1024))
    channel_id = Column("channel_id", Integer)
    msg_id = Column('msg_id', Integer)
    #nlp_id = Column(Integer, ForeignKey('nlp.id'),  nullable=True)
    message = Column('message', VARCHAR(16384)) 
    #message = Column('message', VARCHAR CHECK(length(message) <=500)
    date = Column('date', DateTime)
    #date = Column('date', VARCHAR(1024))
    signature = Column("signature", VARCHAR(1024))
    msg_link = Column('msg_link', VARCHAR(1024))
    views = Column('views', VARCHAR(32))
    number_replies = Column('number_replies', VARCHAR(32))
    number_forwards  = Column('number_forwards', VARCHAR(32))
    is_forward =  Column('is_forward', VARCHAR(32))
    forward_msg_date = Column('forward_msg_date', DateTime)
    forward_msg_date_string =Column('forward_msg_date_string', VARCHAR(32))
    forward_msg_link = Column('forward_msg_link', VARCHAR(1024))
    from_channel_id = Column("from_channel_id", Integer)
    from_channel_name = Column("from_channel_name", VARCHAR(1024))
    is_reply =  Column("is_reply", VARCHAR(32))
    reply_to_msg_id = Column("reply_to_msg_id", VARCHAR(32))
    reply_msg_link = Column('reply_msg_link', VARCHAR(1024))
    contains_media  = Column('contains_media', VARCHAR(32))
    media_type = Column('media_type', VARCHAR(1024))
  

class Tg_channel(Base):
    __tablename__ = 'tele_channel'
    id = Column(Integer, primary_key=True)
    username = Column("username", VARCHAR(1024))
    channel_id = Column("channel_id", VARCHAR(32))
    max_id = Column('max_id', Integer)
    craw_id = Column('craw_id', Integer)

class Tw(Base):
    __tablename__ = 'twitter_channel'
    id = Column(Integer, primary_key=True)
    user_name = Column("user_name", VARCHAR(32))
    active = Column("active", VARCHAR(32))
    display_name = Column("display_name", VARCHAR(32))

class Tw_vd(Base):
    __tablename__ = 'twitter_content'
    id = Column(Integer, primary_key=True)
    publishedat = Column("publishedat", DateTime)
    user_name = Column("user_name",  VARCHAR(255))
    tweet_id = Column("tweet_id",  VARCHAR(255))
    nlp_id = Column(Integer, ForeignKey('nlp.id'), nullable=True)
    text = Column("text",  VARCHAR(16348))
    language = Column("language",  VARCHAR(1024))
    hashtags = Column("hashtags", VARCHAR(1024))
    reply_count = Column("reply_count", Integer)
    retweet_count = Column("retweet_count", Integer)
    like_count = Column("like_count", Integer)
    view_count = Column("view_count", Integer)
    quote_count = Column("quote_count", Integer)
    url = Column("url", VARCHAR(1024))

class All_comment(Base):
    __tablename__ = 'all_comment'
    id = Column(Integer, primary_key=True)
    comment_id = Column("comment_id", Integer)
    network_id = Column("network_id", Integer)
    nlp_id = Column('nlp_id', Integer)
    
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

from transformers import pipeline
classifier = pipeline(task="zero-shot-classification", model="akhtet/mDeBERTa-v3-base-myXNLI", framework="pt")

max_empty_attempts = 10
empty_attempts = 0
while True:
    records_found = False
    a=(DBSession.query(All_comment.id , All_comment.comment_id, All_comment.network_id)
            .filter(All_comment.nlp_id == None)
            #.filter(All_comment.id <= 418258)
            .order_by(All_comment.id.desc()).limit(100))
        
    for row in a:
        records_found = True
        Comment_id =row.comment_id
        Network_id=row.network_id
        ID = row.id
        print("\033[33mAll_comment ID : \033[0m" + f"\033[33m{str(ID)}\033[0m")
        # for facebook
        if (Network_id==1):
            text = DBSession.query(Content.text,Content.id).filter(Content.id == Comment_id).first()
            
            single_line_string = text[0].replace("\n", " ")
            try:
                    fb_post_id = DBSession.query(Comment.post_id).filter(Comment.content_id == text[1]).first()
                    #print(fb_post_id[0])
                    fb_content_id = DBSession.query(Post.content_id).filter(Post.id == fb_post_id[0]).first()
                    print("\033[36mFacebook_Content ID : \033[0m" + f"\033[36m{str(fb_content_id[0])}\033[0m")
                    fb_content = DBSession.query(Content.text,Content.id).filter(Content.id == fb_content_id[0]).first()
                    single_line = fb_content[0].replace("\n", " ")
                    print("\033[36mFacebook_Content : \033[0m" + single_line)
                    print("\033[35mFacebook_Comment ID : \033[0m" + f"\033[35m{text[1]}\033[0m")
                    print("\033[35mFacebook_Comment : \033[0m" + single_line_string)
            except Exception as e:
                        print(KeyError)
                        
            detect = pds.detect(single_line_string)
            if detect == "zg":
                    text=pds.cvt2uni(single_line_string)
            elif detect == "uni":
                    text= text[0]
            #print("\033[35mFacebook_Comment : \033[0m" + text)
            output = classifier(text,
                #candidate_labels=["crime", "business", "entertainment", "social", "politics", "sports", "health", "technology"],
                candidate_labels=["positive", "negative", "neutral"],
            )
            #print (output["sequence"])
            print(f"\033[32m{output['labels'][0]}\033[0m")
            print(output["scores"][0])
            if output['labels'][0]=="positive":
                    res = 1
            if output['labels'][0]=="neutral":
                res = 2
            if output['labels'][0]=="negative":
                res = 3
            if output['labels'][0]=="negative" and output["scores"][0] < 0.50:
                res = 2
                print("neutral")
            print("-------------------------------------------------")
            stmt = (update(All_comment).where(All_comment.id == ID).values(nlp_id=res))
            DBSession.execute(stmt, execution_options={"synchronize_session": False})
            DBSession.commit() 
        
        elif (Network_id==2):
            text = DBSession.query(Yt_cm.text,Yt_cm.id,Yt_cm.youtube_vd_id).filter(Yt_cm.id == Comment_id).first()
            
            youtube_content = DBSession.query(Yt_vd.id, Yt_vd.title).filter(Yt_vd.id == text[2]).first()
            print("\033[36mYoutube_Content ID : \033[0m" + f"\033[35m{str(youtube_content[0])}\033[0m")
            print("\033[36mYoutube_Content : \033[0m" + youtube_content[1])
            print("\033[35mYoutube_Comment ID : \033[0m" + f"\033[35m{text[1]}\033[0m")
            print("\033[35mYoutube_Comment : \033[0m" + text[0])
            detect = pds.detect(text[0])
            if detect == "zg":
                    text=pds.cvt2uni(text[0])
            elif detect == "uni":
                    text= text[0]
            output = classifier(text,
                #candidate_labels=["crime", "business", "entertainment", "social", "politics", "sports", "health", "technology"],
                candidate_labels=[ "positive", "negative","neutral"],
                #candidate_labels=[ "supporting","suggesting","blaming","unsupporting"],
            )
            #print (output["sequence"])
            print(f"\033[32m{output['labels'][0]}\033[0m")
            print(output["scores"][0])
            
            if output['labels'][0]=="positive":
                    res = 1
            if output['labels'][0]=="neutral":
                res = 2
            if output['labels'][0]=="negative":
                res = 3
            if output['labels'][0]=="negative" and output["scores"][0] < 0.50:
                res = 2
                print("neutral")

            print("-------------------------------------------------")
            stmt = (update(All_comment).where(All_comment.id == ID).values(nlp_id=res))
            DBSession.execute(stmt, execution_options={"synchronize_session": False})
            DBSession.commit()
        #sleep(1)
    if not records_found:
        print("No records found with nlp_id set to None.")
        # empty_attempts += 1
        # sleep(1800)
        # if empty_attempts >= max_empty_attempts:
        #     print("Max attempts reached without finding records. Exiting.")
        #     break