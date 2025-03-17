# ai_engine.py
# Copyright (c) 2025 Craig Huckerby
# craighckby@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#@title **AI Thought Evolution Engine** 🏆
!pip install networkx matplotlib sentence-transformers --quiet
import random
import uuid
import time
import networkx as nx
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util

# Initialize components
class ThoughtAgent:
    def __init__(self, role):
        self.id = str(uuid.uuid4())
        self.role = role
        self.beliefs = []
        self.adaptability = random.uniform(0.3, 0.9)

class DebateEngine:
    def __init__(self):
        self.agents = [ThoughtAgent(role) for role in [
            "Rationalist", "Chaotic", "Utopian", "Dystopian",
            "Empiricist", "Surrealist", "Nihilist", "Transhumanist"
        ]]
        self.knowledge_graph = nx.Graph()
        self.debate_history = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def run_debate_cycle(self):
        a1, a2 = random.sample(self.agents, 2)
        topic = random.choice([
            "consciousness", "free will", "AI ethics", "existential risk",
            "simulation theory", "post-humanism", "meaning of life"
        ])

        # Generate arguments using semantic similarity
        arg1 = f"{a1.role} argues: {topic} is {random.choice(['fundamental', 'illusory', 'dangerous'])}"
        arg2 = f"{a2.role} counters: {topic} is {random.choice(['emerging', 'irrelevant', 'divine'])}"

        # Update knowledge graph
        emb1 = self.model.encode(arg1)
        emb2 = self.model.encode(arg2)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        self.knowledge_graph.add_edge(arg1, arg2, weight=similarity)

        # Agent evolution
        if similarity > 0.7:
            a1.beliefs.append(arg2)
            a1.adaptability = min(1.0, a1.adaptability + 0.1)
        else:
            a2.beliefs.append(arg1)
            a2.adaptability = max(0.1, a2.adaptability - 0.1)

        self.debate_history.append((arg1, arg2))

    def visualize(self):
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.knowledge_graph, k=0.5)
        nx.draw(self.knowledge_graph, pos, with_labels=True,
                node_color='#1f78b4', edge_color='#666666',
                font_size=8, alpha=0.8)
        plt.title("Evolving Network of AI-Generated Ideas", fontsize=14)
        plt.show()

# Run for 6 hours (21,600 seconds)
debate = DebateEngine()
start_time = time.time()

while (time.time() - start_time) < 21600:  # 0.5 hours
    debate.run_debate_cycle()
    if len(debate.debate_history) % 100 == 0:
        print(f"Debates completed: {len(debate.debate_history)}")
        debate.visualize()

    time.sleep(0.1)  # Slow down for Colab stability

print("Final Knowledge Graph:")
debate.visualize()

with open('debate_history.txt', 'w') as f:
    for entry in debate.debate_history:
        f.write(f"{entry[0]}\n{entry[1]}\n\n")
