import json
import random

# Define agents and their intents
agents = {
    "youtube": ["youtube_search", "video_recommendation", "youtube_download"],
    "flight": ["flight_search", "flight_booking", "flight_status"],
    "hotel": ["hotel_search", "hotel_booking", "hotel_comparison"],
    "tech_connectivity": ["wifi_troubleshooting", "device_setup", "tech_support"],
    "wellness": ["sleep_tips", "exercise_routine", "health_advice"],
    "financial_wellness": ["budget_planning", "investment_advice", "expense_tracking"],
    "family_care": ["childcare_scheduling", "family_planning", "parenting_tips"],
    "value_assurance": ["price_comparison", "deal_finding", "warranty_registration"],
    "logistics_coordination": ["package_tracking", "delivery_scheduling", "return_processing"],
    "math_solver": ["calculation", "math_problem", "algebra_help"],
    "transit_planning": ["bus_schedule", "train_routes", "public_transit"],
    "uber_booking": ["ride_booking", "taxi_order", "uber_request"],
    "events_discovery": ["event_search", "concert_finder", "local_events"],
    "calendar": ["calendar_management", "meeting_scheduling", "group_calendar"],
    "sports": ["sports_scores", "game_schedule", "team_info"],
    "god_mode": ["complex_planning", "multi_domain", "comprehensive_help"]
}

# Simple Q&A intents with proper answers
simple_qa = [
    ("fact_lookup", "general_qa", ["general_qa"], "Stockholm"),
    ("greeting", "general_qa", ["general_qa"], "Hey there! I'm Arny. How may I assist you today?"),
    ("definition", "general_qa", ["general_qa"], "A global network connecting millions of computers and devices, enabling communication and information sharing worldwide."),
    ("calculation_simple", "math_solver", ["math_solver"], "26")
]

# Proper direct answers for simple queries
direct_answers = {
    "fact_lookup": ["Stockholm", "Amsterdam", "Ottawa", "Rome", "Berlin", "Madrid", "Tokyo", "Canberra"],
    "greeting": ["Hello! I'm Arny, your AI assistant. How can I help?", "Hi! I'm Arny and I'm ready to help. What do you need?", "Good morning! I'm Arny. How may I assist you today?", "Hey there! I'm Arny. What can I do for you?"],
    "definition": ["A global network connecting millions of computers and devices, enabling communication and information sharing worldwide.", "Artificial Intelligence is the simulation of human intelligence in machines that are programmed to think and learn.", "A system of government where power is vested in the people, who rule either directly or through elected representatives.", "Hard Disk Drive - a non-volatile storage device that uses spinning magnetic disks to store and retrieve data."],
    "calculation_simple": ["30", "99", "56", "90", "3", "10", "12", "25"]
}

# Generate user queries
def generate_query(intent, journey):
    templates = {
        "youtube_search": ["Find videos about {}", "Show me {} videos", "YouTube {}"],
        "flight_search": ["Flights from {} to {}", "Book flight to {}", "Flight prices to {}"],
        "hotel_booking": ["Book hotel in {}", "Hotel for {} nights in {}", "Accommodation in {}"],
        "tech_support": ["My {} is not working", "Help with {} setup", "{} troubleshooting"],
        "wellness": ["{} tips", "How to improve {}", "Advice on {}"],
        "financial_wellness": ["{} planning", "Help with {}", "Advice on {}"],
        "math_solver": ["Calculate {}", "Solve {}", "Math problem: {}"],
        "ride_booking": ["Book Uber to {}", "Ride to {}", "Taxi from {} to {}"],
        "calendar_management": ["Schedule meeting {}", "Add to calendar {}", "Calendar for {}"],
        "complex_planning": ["Plan a trip to {}", "Help with {} and {}", "Comprehensive {}"]
    }
    
    topics = ["Paris", "math", "wifi", "sleep", "budget", "family", "deals", "delivery", "algebra", "bus", "concert", "meeting", "sports", "everything"]
    topic = random.choice(topics)
    
    if intent in templates:
        template = random.choice(templates[intent])
        return template.format(topic, topic)
    else:
        return f"{intent.replace('_', ' ')} help"

# Generate entry
def generate_entry():
    # 70% agent-specific, 30% simple QA
    if random.random() < 0.7:
        journey = random.choice(list(agents.keys()))
        intent = random.choice(agents[journey])
        primary_journey = journey
        journeys = [journey]
        direct_answer = None
        needs_execution = True
        execution_type = "cloud_agent"
        complexity_score = random.randint(20, 80)
        formatting_style = "confirmation_summary"
    else:
        intent, primary_journey, journeys, sample_answer = random.choice(simple_qa)
        direct_answer = random.choice(direct_answers[intent])
        needs_execution = False
        execution_type = None
        complexity_score = random.randint(1, 10)
        formatting_style = "single_word" if intent == "fact_lookup" else "greeting_response" if intent == "greeting" else "short_definition"
    
    user_query = generate_query(intent, primary_journey)
    
    # Missing fields
    missing_fields = []
    needs_clarification = False
    clarification = None
    if random.random() < 0.3 and not direct_answer:
        possible_missing = ["date", "location", "guests", "budget", "details"]
        missing_fields = random.sample(possible_missing, random.randint(1, 3))
        needs_clarification = True
        clarification = f"Please provide: {', '.join(missing_fields)}"
        needs_execution = False
        execution_type = None
        complexity_score = random.randint(15, 45)
        formatting_style = "clarification_prompt"
    
    routing_confidence = round(random.uniform(0.7, 0.99), 2)
    
    entry = {
        "messages": [
            {
                "role": "system",
                "content": "You are Arny's Tier-1 Router Model.\n\nYour job:\n- Decide what should happen next for a user query\n- Output STRICT JSON using the agreed schema\n- Answer directly ONLY if the answer is atomic\n- Never explain\n- Never chat\n- Ask clarification ONLY if required fields are missing"
            },
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "assistant",
                "content": json.dumps({
                    "intent": intent,
                    "primary_journey": primary_journey,
                    "journeys": journeys,
                    "direct_answer": direct_answer,
                    "missing_fields": missing_fields,
                    "needs_clarification": needs_clarification,
                    "clarification": clarification,
                    "needs_execution": needs_execution,
                    "execution_type": execution_type,
                    "complexity_score": complexity_score,
                    "routing_confidence": routing_confidence,
                    "formatting_style": formatting_style
                })
            }
        ]
    }
    return entry

# Generate 3000 entries
entries = [generate_entry() for _ in range(3000)]

# Write to file
with open("new_entries_fixed.jsonl", "w") as f:
    for entry in entries:
        f.write(json.dumps(entry) + "\n")

print("Generated 3000 new entries with proper direct answers in new_entries_fixed.jsonl")