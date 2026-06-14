import logging
import google.generativeai as genai

logger = logging.getLogger(__name__)

class FallbackGenerativeModel:
    """
    A transparent proxy class that behaves exactly like genai.GenerativeModel,
    but wraps generate_content() and start_chat() in an intelligent try-except block.
    If a quota/429 error is hit on the primary model, it instantly and silently retries 
    the exact same payload on the fallback model.
    """
    def __init__(self, primary_model_name="gemini-2.5-flash", fallback_model_name="gemini-2.5-flash-lite", **kwargs):
        self.primary_model_name = primary_model_name
        self.fallback_model_name = fallback_model_name
        self.kwargs = kwargs
        
        self.primary_model = genai.GenerativeModel(primary_model_name, **kwargs)
        self.fallback_model = genai.GenerativeModel(fallback_model_name, **kwargs)

    def generate_content(self, *args, **kwargs):
        try:
            return self.primary_model.generate_content(*args, **kwargs)
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "exhausted" in err_str:
                logger.warning("Quota exceeded on %s. Autonomously falling back to %s.", self.primary_model_name, self.fallback_model_name)
                return self.fallback_model.generate_content(*args, **kwargs)
            raise e

    def start_chat(self, *args, **kwargs):
        return FallbackChatSession(self, *args, **kwargs)

class FallbackChatSession:
    """
    Wraps the genai ChatSession string logic. 
    If a chat.send_message() fails mid-session, it instantiates 
    the fallback model, ports the chat history over precisely, 
    and resends the message.
    """
    def __init__(self, fallback_generative_model, *args, **kwargs):
        self.fallback_model = fallback_generative_model
        self.args = args
        self.kwargs = kwargs
        self.primary_chat = fallback_generative_model.primary_model.start_chat(*args, **kwargs)
        self._is_fallen_back = False
        self.fallback_chat = None

    @property
    def history(self):
        if self._is_fallen_back:
            return self.fallback_chat.history
        return self.primary_chat.history

    def send_message(self, *args, **kwargs):
        if self._is_fallen_back:
            return self.fallback_chat.send_message(*args, **kwargs)
            
        try:
            return self.primary_chat.send_message(*args, **kwargs)
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "exhausted" in err_str:
                logger.warning("Quota exceeded during chat on %s. Migrating history and falling back to %s.", 
                               self.fallback_model.primary_model_name, self.fallback_model.fallback_model_name)
                self._is_fallen_back = True
                # Migrate history securely from the failed instance
                self.kwargs['history'] = self.primary_chat.history
                self.fallback_chat = self.fallback_model.fallback_model.start_chat(*self.args, **self.kwargs)
                return self.fallback_chat.send_message(*args, **kwargs)
            raise e
