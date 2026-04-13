"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Your input ->  Hey! Calling to confirm a booking                                                                                                                                                                 
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                        
And how many of those guests will need vegan meals?
Your input ->  ~50 vegan                                                                                                                                                                                         
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200                                                                                                                                                                                              
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
"""

CONVERSATION_1_OUTCOME = "confirmed"   # "confirmed" or "escalated"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Your input ->  Hey, calling to confirm a booking                                                                                                                                                                 
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                        
And how many of those guests will need vegan meals?
Your input ->  ~50                                                                                                                                                                                               
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £350                                                                                                                                                                                              
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £350 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
"""

CONVERSATION_2_OUTCOME = "escalated"   # "confirmed" or "escalated"
CONVERSATION_2_REASON  = "a deposit of £350 exceeds the organiser's authorised limit of £300"   # the reason the agent gave for escalating

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Your input ->  Hello, calling to confirm a booking                                                                                                                                                               
How many guests are you confirming for tonight's event?
Your input ->  160 guests                                                                                                                                                                                        
And how many of those guests will need vegan meals?
Your input ->  Sorry, before we continue, could you confirm whether you have AV equipment available?                                                                                                             
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
It switched to a utter_out_of_scope flow, that triggered agent to response "I'm sorry, I'm not trained to help with that." 
and then asked whether the user wants to continue. 
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
It's much more clear message for the human and it's much better user experience. Instead of generating a message on 
flight it has specific flow to handle out of scope requests. Although the message still generic and it's not perfectly
clear what requests are out of scope and why.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True   # True or False

# List every file you changed.
TASK_B_FILES_CHANGED = ['exercise3_rasa/actions/actions.py']

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I tested the cutoff guard by simulating a user request at different times of the day. I verified that the guard correctly
escalates the conversation when the time is past 16:45 and prevents further processing of the confirmation request.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
Old Rasa was deterministic, you could trace every decision to a specific rule or pattern.

In new Rasa the LLM handles the extraction of values, interpret user intent and trigger flows.

The trust in the LLM's ability to understand and interpret user requests has shifted, but Python's role remains crucial 
for enforcing business logic and maintaining data integrity.

The old approach is definitely more reproducible, cheaper to run, easier to maintain, and has lower latency.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
CALM cannot reach for a tool that wasn't wired up at design time. Every capability 
must be declared: actions, slots, endpoints. LangGraph can bind tools dynamically and let the LLM decide when to use them.

CALM flows are linear-ish sequences with limited branching. Complex reasoning chain are simply not possible.

Rasa CALM requires more setup and is less flexible, but for a narrow use case such as booking confirmation, 
that can be a feature. CALM handles out-of-scope requests more reliably than LangGraph. It won't hallucinate, 
produce confusing responses, or perform unnecessary actions.
"""
