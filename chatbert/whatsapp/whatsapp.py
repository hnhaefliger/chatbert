from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from chatbert import utils
import os
import time

class User:
    def __init__(self):
        self.driver = None
        self.chats = None
        self.current_chat = None

    def start(self):
        if self.driver == None:
            self.driver = webdriver.Chrome(os.path.dirname(__file__) + '/../drivers/chromedriver') # open chrome browser
            self.driver.get('http://web.whatsapp.com') # navigate to whatsapp

        try:
            self.driver.find_element_by_xpath('.//div[@class="_1yHR2"]') # the canvas with the login code
            return False # the user has not logged in yet

        except:
            self.chats = self.getChats() # get a list of chats for later error handling
            return True

    def close(self):
        self.driver.close()

    def getChats(self): # get a list of all available chats
        if self.driver == None:
            raise Exception('no driver yet') # error handling - todo
        
        chats = [] # collective list of all chats
        
        chatbox = utils.waitForXPathLoad(self.driver, './/div[@class="_3Xjbn _3jNGW"]')[0] # box containing all chat titles
        max_scroll_height = self.driver.execute_script('return arguments[0].scrollHeight;', chatbox) # maximum scroll

        for i in range(0, max_scroll_height, 1000): # need to scroll so that every chat loads
            self.driver.execute_script('arguments[0].scrollTo(0, arguments[1]);', chatbox, i) # scroll down

            tmp_chats = utils.waitForXPathLoad(chatbox, './/span[@class="_1hI5g _1XH7x _1VzZY"]') # wait for the chats to load
            tmp_chats = [utils.waitForAttributeLoad(chat, 'title') for chat in tmp_chats] # get chat titles
            tmp_chats = [chat for chat in tmp_chats if chat != ''] # get all non blank chat titles

            for chat in tmp_chats: # add new chats to collective list
                if not(chat in chats):
                    chats.append(chat)

        self.driver.execute_script('arguments[0].scrollTo(0, arguments[1]);', chatbox, 0) # scroll back to top
        
        return chats

    def openChat(self, chat_name):
        if chat_name in self.chats: # check that a valid chat name was provided
            chatbox = utils.waitForXPathLoad(self.driver, './/div[@class="_3Xjbn _3jNGW"]')[0] # box containing all chat titles
            max_scroll_height = self.driver.execute_script('return arguments[0].scrollHeight;', chatbox) # maximum scroll
            
            for i in range(0, max_scroll_height, 1000): # need to scroll so that every chat loads
                self.driver.execute_script('arguments[0].scrollTo(0, arguments[1]);', chatbox, i) # scroll down
                tmp_chats = utils.waitForXPathLoad(chatbox, './/span[@class="_1hI5g _1XH7x _1VzZY"]') # wait for chats to load
                chats = utils.waitForXPathLoad(chatbox, './/div[@class="_1MZWu"]') # get clickables

                for chat in chats: # find the correct clickable
                    inner = utils.waitForAttributeLoad(chat, 'innerHTML')
                    inner = inner[inner.index('title="'):inner.index('class="_1hI5g _1XH7x _1VzZY"')] # find the location of the chat name
                    
                    if chat_name in inner: # check if the chat name is in this element
                        chat.click() # open the chat
                        self.current_chat = chat_name
                        return None # end the loops
            
        else:
            raise ValueError('The chat "', chat_name, '" does not exist') # if an invalid chat name was provided

    def sendMessage(self, message):
        if self.current_chat != None: # check that there is currently a chat open
            msg_box = utils.waitForXPathLoad(self.driver, './/div[@class="_1awRl copyable-text selectable-text"]')[-1] # the chat text box
            msg_box.send_keys(message) # type the message
            msg_box.send_keys(Keys.ENTER) # send the message
            
        else:
            raise Exception('no chat selected - this is a placeholder for now')

    def getMessages(self, n=1):
        # to-do: there is an error if the other users send a message at exactly the right time (wait for messages to load)
        # to-do: scroll up to get more chats
        # to-do: optimize loading time
        
        if self.current_chat != None: # check that there is currently a chat open
            msgs_box = utils.waitForXPathLoad(self.driver, './/div[@class="tSmQ1"]')[0] # the box containing all messages

            # scroll up loop
            messages = utils.waitForXPathLoad(msgs_box, './/div[@data-id][@tabindex]') # get every loaded message
            valid_messages = messages

            '''[]
            
            for message in messages: # filter out the whatsapp floating time and recalled and deleted messages
                try:
                    valid_messages.append(message.find_element_by_xpath('.//div[@data-pre-plain-text]'))
                    
                except:
                    pass
            '''
                
            messages_data = [utils.waitForAttributeLoad(message, 'data-pre-plain-text') for message in valid_messages] # message sender and timestamp
            messages_data = [message[1:-2].split('] ') for message in messages_data] # split timestamp and sender
            
            messages = [utils.waitForXPathLoad(message, './/span')[0] for message in valid_messages]
            print(messages)
            messages = [utils.waitForXPathLoad(message, './/span')[0] if 'span' in utils.waitForAttributeLoad(message, 'innerHTML') else '' for message in messages]
            messages = [utils.waitForAttributeLoad(message, 'innerHTML') if message != '' else '<img>' for message in messages] # message text or tag for only image messages
            images = [utils.findImages(message) for message in messages]
            
            return messages, messages_data

        else:
            raise Exception('no chat selected - this is a placeholder for now')


