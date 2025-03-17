# -*- coding: utf-8 -*-
#
# Copyright (c) 2024 [Craig Huckerby]. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @title **AI Thought Evolution Engine** 🏆
!pip install networkx matplotlib sentence-transformers --quiet

import random
import uuid
import time
import networkx as nx
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util

class ThoughtAgent:
    """Represents an agent in the thought evolution engine."""
    def __init__(self, role):
        self.id = str(uuid.uuid4())
        self.role = role
        self.beliefs = []
        self.adaptability = random.uniform(0.3, 0.9)

class DebateEngine:
    """Manages the debate process among thought agents."""
    def __init__(self):
        self.agents = [ThoughtAgent(role) for role in [
            "Rationalist", "Chaotic", "Utopian", "Dystopian",
            "Empiricist", "Surrealist", "Nihilist", "Transhumanist"
        ]]
        self.knowledge_graph = nx.Graph()
        self.debate_history = []
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def run_debate_cycle(self):
        """Runs a debate cycle between two randomly selected agents on a chosen topic."""
        if len(self.agents) < 2:
            return  # Ensure there are at least two agents

        a1, a2 = random.sample(self.agents, 2)
        topic = random.choice([
            "consciousness", "free will", "AI ethics", "existential risk",
            "simulation theory", "post-humanism", "meaning of life"
        ])

        # Generate arguments based on the topic
        arg1 = f"{a1.role} argues: {topic} is {random.choice(['fundamental', 'illusory', 'dangerous'])}."
        arg2 = f"{a2.role} counters: {topic} is {random.choice(['emerging', 'irrelevant', 'divine'])}."

        # Calculate semantic similarity using embeddings
        emb1 = self.model.encode(arg1, convert_to_tensor=True)
        emb2 = self.model.encode(arg2, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb1, emb2).item()

        # Update knowledge graph
        self.knowledge_graph.add_edge(arg1, arg2, weight=similarity)

        # Agent evolution based on similarity
        if similarity > 0.7:
            a1.beliefs.append(arg2)
            a1.adaptability = min(1.0, a1.adaptability + 0.1)
        else:
            a2.beliefs.append(arg1)
            a2.adaptability = max(0.1, a2.adaptability - 0.1)

        self.debate_history.append((arg1, arg2))

    def visualize(self):
        """Visualizes the knowledge graph of debates."""
        plt.figure(figsize=(16, 12))
        pos = nx.spring_layout(self.knowledge_graph, k=0.5)
        nx.draw(self.knowledge_graph, pos, with_labels=True,
                node_color='#1f78b4', edge_color='#666666',
                font_size=8, alpha=0.8)
        plt.title("Evolving Network of AI-Generated Ideas", fontsize=14)
        plt.show()

# --- Main Execution Block ---

if __name__ == "__main__":
    # Initialize the debate engine
    debate = DebateEngine()

    # Set runtime for the simulation to 20 minutes (1200 seconds)
    runtime_seconds = 1200  # 20 minutes
    start_time = time.time()

    # Open a log file to record progress
    with open('debate_progress.log', 'w') as log_file:
        while (time.time() - start_time) < runtime_seconds:
            debate.run_debate_cycle()
            debate_count = len(debate.debate_history)

            # Log progress every 100 debates
            if debate_count % 100 == 0:
                log_file.write(f"Debates completed: {debate_count}\n")
                log_file.flush()  # Ensure data is written to file

            time.sleep(0.1)  # Slow down to maintain stability

    print("Final Knowledge Graph:")
    debate.visualize()

    # Save the debate history to a text file
    with open('debate_history.txt', 'w') as f:
        for entry in debate.debate_history:
            f.write(f"{entry[0]}\n{entry[1]}\n\n")
