from dotenv import load_dotenv
from groq import Groq
import os, json

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def extract_action_items(transcript: str) -> list:
    """
    Takes a call transcript.
    Returns a list of action items as JSON.
    """
    if not transcript.strip():
        return []

    prompt = f"""
You are analyzing a customer support call transcript.
Extract all action items — things that need to be done after the call.
Return ONLY a JSON array like this:
[
  {{"action": "Send refund form to customer", "deadline": "today"}},
  {{"action": "Call back tomorrow at 3 PM", "deadline": "tomorrow 3 PM"}}
]
If no action items, return: []

TRANSCRIPT:
{transcript}
"""
    response = client.chat.completions.create(
        model='llama3-8b-8192',
        temperature=0.0,
        messages=[{'role':'user','content':prompt}],
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except:
        return [{"action": raw, "deadline": "unknown"}]

# Test it
if __name__ == "__main__":
    test = '''
    Agent: I will send you the refund form by email today.
    Customer: Also please call me back tomorrow at 3 PM.
    Agent: Sure, I will escalate this to the manager as well.
    '''
    items = extract_action_items(test)
    print(json.dumps(items, indent=2))
    print("\n--- TESTING 3 TRANSCRIPTS ---\n")

    # Test 1 - Simple
    t1 = "Agent: I will email you the invoice. Customer: Thank you."
    print("Test 1:", extract_action_items(t1))

    # Test 2 - Multiple actions
    t2 = "Agent: I will process refund in 3-5 days. I will also send confirmation email and escalate your complaint to supervisor."
    print("Test 2:", extract_action_items(t2))

    # Test 3 - No action items
    t3 = "Agent: Hello. Customer: Never mind it is already solved. Agent: Great have a nice day."
    print("Test 3:", extract_action_items(t3))