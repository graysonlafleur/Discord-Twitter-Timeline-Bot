#created by Grayson LaFleur

import tweepy, json

f = open('C:\\Users\\vidrinen\Desktop\\API keys\\twitterAPI.json')

data = json.load(f)

key = data.get("key")
secret = data.get("secret")
consumer_key = data.get("consumer_key")
consumer_secret = data.get("consumer_secret")

# users - used for keeping screen names so that follower_list() can display normal links
# userIDs - used for searching the twitter streamlistener since it requires ids
# links - links to tweets as they come through the streamlistener, resets every time it populates
users = []
userIDs = []
links = []

#UserError super class, extends Exception
class UserError(Exception):
    """Raises an exception anytime the user makes an error

    Attributes:
        message -- explaination of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

#UserError children classes
class UserAlreadyExists(UserError):
    
    """Exception raised because the user already exists in the follow list

    Attributes:
        user -- the user attempting to be added to the follower list
        message -- explaination of the error
    """

    def __init__(self, user):
        self.message = f"{user} is already in your follow list"
        super().__init__(self.message)
class UserDoesNotExist(UserError):
    
    """Exception raised because the user doesn't exist in the follow list

    Attributes:
        user -- the user attempting to be removed from the follower list
        message -- explaination of the error
    """

    def __init__(self, user):
        self.message = f"{user} is not in your follower list"
        super().__init__(self.message)
class UsersEmpty(UserError):
    
    """Exception raised because the user doesn't exist in the follow list

    Attributes:
        user -- the user attempting to be removed from the follower list
        message -- explaination of the error
    """

    def __init__(self):
        self.message = "You are not following anyone"
        super().__init__(self.message)

#Constantly looks through the accounts given to see if they have sent out a tweet
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.id_str in userIDs:
            links.append(f'https://twitter.com/{status.user.screen_name}/status/{status.id_str}')

    def on_error(self, status_code):
        return super().on_error(status_code)

class TwitterAPI:

    def __init__(self):
        self.auth = tweepy.OAuthHandler(key, secret)
        self.auth.set_access_token(consumer_key, consumer_secret)

        self.api = tweepy.API(self.auth)

    def start_stream_listener(self):
        myStreamListener = MyStreamListener()
        self.myStream = tweepy.Stream(auth = self.api.auth, listener=myStreamListener)
        self.myStream.filter(follow=userIDs, is_async=True)

    def add_follower(self, user):
        if self.verify_user(user)== True:
            userID = self.api.get_user(user).id_str
            if user not in users:
                users.append(user)
                userIDs.append(userID)
                self.myStream.disconnect()
                self.start_stream_listener()
            else:
                raise UserAlreadyExists(user)
        else:
            raise UserDoesNotExist(user)

    def remove_follower(self, user):
        if self.verify_user(user) == True:
            if user in users:
                userID = self.api.get_user(user).id_str
                users.remove(user)
                userIDs.remove(userID)
                self.myStream.disconnect()
                self.start_stream_listener()
            else:
                raise UserDoesNotExist(user)
        else:
            raise UserDoesNotExist(user)

    def follower_list(self):
        if len(users) > 0:
            return users
        else:
            raise UsersEmpty()

    #checks if the user exists
    def verify_user(self, user):
        try:
            self.api.get_user(user)
        except Exception:
            return False
        return True

    #gives the links to the tweets from the people you're following to the DiscordAPI
    def get_urls(self):
        if len(links) > 0:
            temp = links
            return temp
    
    def clear_links(self):
        links.clear()