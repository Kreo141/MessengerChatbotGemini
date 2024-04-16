from fbchat import Client
from fbchat.models import Message, ThreadType
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

class MessBot(Client):
    def __init__(self, email, password, session_cookies):
        super().__init__(email, password, session_cookies=session_cookies)

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        try:
            msg = str(message_object).split(",")[15][14:-1]
            print(msg)
            if "//video.xx.fbcdn" not in msg:
                msg = str(message_object).split(",")[19][20:-1]
        except Exception as e:
            try:
                msg = message_object.text.lower()
                print(msg)
            except AttributeError:
                pass

        if author_id != self.uid:
            if "hi" in msg:
                self.send(Message(text="Hello"), thread_id=thread_id, thread_type=thread_type)
            elif "how are you" in msg:
                self.send(Message(text="Good!"), thread_id=thread_id, thread_type=thread_type)
            else:
                messages = ["NEXT REQUEST", msg]
                response = genai.chat(**defaults, messages=messages)
                ai_response = response.last
                self.send(Message(text=ai_response), thread_id=thread_id, thread_type=thread_type)

session_cookies = {
    "sb": "",
    "fr": "",
    "c_user": "",
    "datr": "",
    "xs": ""
}

client = MessBot("EMAIL", "PASS", session_cookies=session_cookies)
print(client.isLoggedIn())

try:
    client.listen()
except KeyboardInterrupt:
    print("Interrupted")
