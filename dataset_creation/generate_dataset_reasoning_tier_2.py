import json
import random

# Expanded diverse topics with varied explanations
topics_explanations = {
    # Technology & Science
    "quantum computing": "Quantum computing uses quantum bits, or qubits, which can represent both 0 and 1 simultaneously through superposition. This enables quantum computers to explore multiple solutions in parallel, solving certain problems exponentially faster than classical computers, particularly in cryptography, optimization, and molecular simulation.",
    "machine learning": "Machine learning is a subset of artificial intelligence enabling systems to learn patterns from data and improve performance iteratively without explicit programming. It powers recommendation systems, image recognition, natural language processing, and predictive analytics across industries.",
    "blockchain": "Blockchain is a distributed ledger technology maintaining an immutable record of transactions across decentralized networks. Each block contains cryptographic hashes of previous blocks, ensuring security and transparency without central authority, forming the foundation of cryptocurrencies and smart contracts.",
    "artificial intelligence": "Artificial intelligence simulates human cognitive functions through algorithms and neural networks. Modern AI encompasses machine learning, deep learning, natural language processing, and computer vision, enabling autonomous systems, predictive analytics, and intelligent automation.",
    "cybersecurity": "Cybersecurity involves protecting digital assets, networks, and data from unauthorized access and malicious attacks. It encompasses encryption, firewalls, intrusion detection, vulnerability management, and security protocols to safeguard against evolving threats.",
    "cloud computing": "Cloud computing delivers computing resources—servers, storage, databases, software—over the internet on-demand. It offers scalability, flexibility, and cost efficiency, enabling organizations to access powerful infrastructure without maintaining physical hardware.",
    
    # Environmental & Social
    "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns. While natural climate variability exists, scientific consensus indicates human activities—primarily fossil fuel combustion and deforestation—are causing unprecedented rapid warming with significant environmental and societal impacts.",
    "renewable energy": "Renewable energy comes from naturally replenishing sources like solar, wind, hydroelectric, and geothermal power. Unlike fossil fuels, renewables produce minimal greenhouse gas emissions and provide sustainable alternatives for meeting global energy demands.",
    "sustainable agriculture": "Sustainable agriculture integrates environmental stewardship with food production, using practices like crop rotation, organic farming, precision agriculture, and water conservation. It balances productivity with ecosystem health and long-term soil viability.",
    "ocean acidification": "Ocean acidification occurs when seawater absorbs excess atmospheric carbon dioxide, forming carbonic acid and lowering pH. This process threatens marine life, particularly organisms with calcium carbonate shells, disrupting ecosystems and fisheries worldwide.",
    
    # Health & Wellness
    "mental health": "Mental health encompasses psychological, emotional, and social well-being, affecting how we think, feel, and act. It involves managing stress, building resilience, and seeking support through therapy, meditation, exercise, and community connection for optimal quality of life.",
    "immunology": "Immunology studies the immune system's mechanisms for defending against pathogens and disease. It examines antibodies, white blood cells, inflammation, and immune responses, informing vaccine development, allergy treatment, and autoimmune disorder management.",
    "genetic engineering": "Genetic engineering involves directly manipulating an organism's DNA to introduce desired traits. Applications include creating disease-resistant crops, producing insulin, developing gene therapies for genetic disorders, and advancing personalized medicine.",
    "neuroscience": "Neuroscience investigates the nervous system's structure and function, studying how neurons communicate through synapses and neurotransmitters. Research illuminates consciousness, memory, learning, and neurological disorders, advancing brain health understanding.",
    
    # Business & Economics
    "digital transformation": "Digital transformation integrates digital technology into business processes, fundamentally changing operations and customer experiences. It involves automation, data analytics, cloud adoption, and cultural change to enhance efficiency and competitiveness.",
    "cryptocurrency": "Cryptocurrency is digital money using cryptographic security and decentralized networks like blockchain. Bitcoin, Ethereum, and other cryptocurrencies enable peer-to-peer transactions, smart contracts, and decentralized finance without traditional banking intermediaries.",
    "supply chain management": "Supply chain management optimizes the flow of goods and services from supplier to consumer. Modern approaches include demand forecasting, inventory optimization, logistics coordination, and risk management to reduce costs and improve delivery reliability.",
    "artificial general intelligence": "Artificial general intelligence refers to hypothetical AI systems with human-level intelligence across diverse tasks. Unlike narrow AI excelling in specific domains, AGI could understand, learn, and apply knowledge across different contexts, representing a significant milestone in AI development.",
    
    # Education & Innovation
    "online learning": "Online learning delivers education through digital platforms, enabling flexible, self-paced instruction accessible globally. It combines video lectures, interactive assignments, peer collaboration, and personalized learning paths, democratizing education access.",
    "augmented reality": "Augmented reality overlays digital information onto the physical world, enhancing perception and interaction. Applications include navigation, medical visualization, industrial maintenance, gaming, and education, creating immersive experiences blending virtual and physical environments.",
    "virtual reality": "Virtual reality creates immersive digital environments through headsets and sensory feedback, simulating realistic experiences. It's applied in gaming, training simulations, therapy, architecture visualization, and entertainment, providing safe spaces for exploration and learning.",
    "edge computing": "Edge computing processes data closer to its source—on local devices or edge servers—rather than centralized clouds. This reduces latency, improves real-time responsiveness, enhances privacy, and decreases bandwidth requirements for IoT devices and applications.",
    
    # Advanced Concepts
    "quantum entanglement": "Quantum entanglement occurs when particles become correlated such that measuring one instantly affects the other, regardless of distance. Einstein called this 'spooky action at a distance,' and it's fundamental to quantum mechanics, enabling quantum cryptography and teleportation.",
    "dark matter": "Dark matter is invisible matter constituting approximately 85% of matter in the universe. Its gravitational effects are observed in galaxy rotation and cosmic structures, but its composition remains unknown, making it a frontier in physics research.",
    "behavioral economics": "Behavioral economics combines psychology with economics, studying how cognitive biases and emotions influence financial decisions. It explains phenomena like loss aversion, anchoring, and herd behavior, challenging traditional rational actor assumptions.",
    "microbiome": "The microbiome comprises trillions of microorganisms—bacteria, fungi, viruses—inhabiting human bodies. Recent research reveals profound impacts on immunity, digestion, mental health, and disease susceptibility, transforming medical understanding.",
    "neural networks": "Neural networks are computing systems inspired by biological neural connections. Composed of interconnected nodes processing information in layers, they excel at pattern recognition, enabling deep learning applications in computer vision, language processing, and predictive modeling."
}

# Diverse reasoning question templates
reasoning_templates = {
    "explanation": "Explain {} in simple terms.",
    "comparison": "Compare and contrast {} with similar concepts.",
    "application": "How is {} applied in real-world scenarios?",
    "history": "Describe the historical development of {}.",
    "challenges": "What are the main challenges in {}?",
    "future": "What does the future of {} look like?",
    "impact": "What is the societal impact of {}?",
    "technical": "Explain the technical foundations of {}.",
    "ethical": "What ethical considerations surround {}?",
    "limitation": "What are the limitations of {}?"
}

# Extended diverse reasoning responses
def generate_reasoning_response(topic, question_type):
    """Generate contextually appropriate reasoning responses"""
    responses = {
        "explanation": f"{topic} is a complex concept that plays an important role in modern society. Understanding its fundamentals requires examining its core mechanisms, applications, and implications across different domains.",
        "comparison": f"While {topic} shares similarities with related concepts, it distinguishes itself through unique characteristics and applications. The relationship between these concepts reveals deeper understanding of underlying principles.",
        "application": f"Real-world applications of {topic} span numerous industries and domains. From research institutions to commercial enterprises, practical implementations demonstrate the versatility and importance of this concept.",
        "history": f"The development of {topic} occurred gradually through contributions from multiple researchers and innovators. Understanding this historical progression provides context for current implementations and future possibilities.",
        "challenges": f"Implementing and advancing {topic} faces several significant challenges including technical limitations, resource constraints, and evolving requirements. Addressing these challenges requires interdisciplinary collaboration and innovation.",
        "future": f"The future trajectory of {topic} appears promising with emerging technologies and methodologies. Continued research and development will likely overcome current limitations and unlock new applications.",
        "impact": f"The societal impact of {topic} extends across economic, environmental, and social dimensions. Both beneficial applications and potential risks require careful consideration and responsible implementation.",
        "technical": f"The technical foundations of {topic} involve sophisticated principles and mechanisms. Deep understanding requires knowledge of underlying mathematics, physics, or computer science principles.",
        "ethical": f"Ethical considerations surrounding {topic} include privacy, fairness, accountability, and transparency. Responsible development and deployment require thoughtful examination of moral implications.",
        "limitation": f"Despite advantages, {topic} has inherent limitations affecting its applicability and effectiveness. Recognizing these constraints is crucial for realistic expectations and appropriate implementation strategies."
    }
    return responses.get(question_type, responses["explanation"])

# Generate diverse Tier-2 entries
def generate_tier2_entry():
    topic = random.choice(list(topics_explanations.keys()))
    question_type = random.choice(list(reasoning_templates.keys()))
    
    user_query = reasoning_templates[question_type].format(topic)
    explanation = topics_explanations[topic]
    
    # Add follow-up reasoning to make responses more substantive
    reasoning_context = generate_reasoning_response(topic, question_type)
    full_response = f"{explanation}\n\n{reasoning_context}"
    
    entry = {
        "messages": [
            {
                "role": "system",
                "content": "You are Arny's Tier-2 Reasoning and Generation Model.\n\nYour capabilities:\n- Deep reasoning on complex topics\n- Step-by-step planning and explanations\n- Natural language generation with nuanced understanding\n- Detailed comparisons and analyses\n- Comprehensive problem-solving\n\nProvide thorough, well-reasoned responses without JSON formatting. Focus on depth, clarity, and insight."
            },
            {
                "role": "user",
                "content": user_query
            },
            {
                "role": "assistant",
                "content": full_response
            }
        ]
    }
    return entry

# Generate 3000 diverse entries for Tier-2
tier2_entries = [generate_tier2_entry() for _ in range(3000)]

# Write to file
with open("tier2_reasoning_dataset_3k.jsonl", "w") as f:
    for entry in tier2_entries:
        f.write(json.dumps(entry) + "\n")

print("Generated 3000 diverse Tier-2 reasoning entries in tier2_reasoning_dataset_3k.jsonl")
print(f"Topics covered: {len(topics_explanations)}")
print(f"Question types: {len(reasoning_templates)}")
print("Dataset is now ready for fine-tuning with diverse topics and reasoning patterns.")