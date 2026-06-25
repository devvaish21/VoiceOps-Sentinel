from gtts import gTTS

text = """
Agent: Thank you for calling FastPay customer support. My name is Priya. How can I help you today?

Customer: Hi Priya. I have a serious problem. I was charged three times for my monthly subscription and I want a refund immediately.

Agent: I completely understand your concern and I sincerely apologize for the inconvenience. May I have your registered email address to pull up your account?

Customer: Sure. It is john dot smith at gmail dot com.

Agent: Thank you John. I can see your account here. You are right, there are three duplicate charges from this month. I am really sorry about that.

Customer: This is unacceptable. I have been a customer for two years and this has never happened before. I am thinking of cancelling my subscription.

Agent: I completely understand John and I take full responsibility. I will process a full refund for all three duplicate charges right now. You will receive the amount within 3 to 5 business days.

Customer: Okay. And what about my subscription? Will it still be active?

Agent: Absolutely. Your subscription remains fully active. We will also add one month free as compensation for this inconvenience.

Customer: Oh okay. That is actually very kind. Thank you.

Agent: You are most welcome John. Is there anything else I can help you with today?

Customer: No that is all. Thank you Priya.

Agent: Thank you for your patience John. Have a wonderful day. Goodbye.
"""

tts = gTTS(text, lang="en")
tts.save("sample_call.mp3")
print("Done! sample_call.mp3 created.")