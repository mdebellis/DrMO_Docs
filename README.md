# SAAKSHII: Ontology-Grounded Dental Materials RAG System

**SAAKSHII** is a women-led AI initiative that combines structured clinical knowledge with modern Large Language Models (LLMs) to improve the accuracy, transparency, and safety of information retrieval in dentistry.

The system integrates:
- A clinically curated **Dental Restorative Materials Ontology**
- A **Knowledge Graph** derived from evidence-based dental documents
- A **Retrieval-Augmented Generation (RAG)** pipeline grounded in ontology structure
- A simple **Streamlit interface** for clinician-friendly interaction

This project demonstrates how ontology-driven knowledge representation can
reduce hallucinations, increase factual accuracy, and support safe adoption
of LLM-based tools in dental practice.

---

## 🌟 What “SAAKSHII” Represents

**SAAKSHII** is both:

- A **Hindi word** meaning *witness*, *evidence*, or *one who bears reliable knowledge*  
- An **acronym** chosen by the team to reflect its mission  
  *(Exact expansion added after final team confirmation — placeholder below)*

> **SAAKSHII**: *[Safe AI and Knowledge-Supported Healthcare Information Interface]*  
*(Replace with final agreed acronym if different.)*

The name captures the system’s purpose:  
**to provide evidence-grounded, transparent AI assistance for clinicians.**

---

## 🧠 Project Overview

Modern LLMs are powerful but prone to:
- hallucinations  
- inconsistent reasoning  
- lack of source attribution  
- limited clinical accountability  

Dentistry lacks the structured knowledge resources (similar to RxNorm or SNOMED CT in medicine) needed to ensure trustworthy AI responses about materials and products.

**SAAKSHII addresses this gap** by combining symbolic knowledge (ontology + knowledge graph) with neural methods (LLM embeddings + RAG).

---

## 🧪 Components

### **1. Dental Restorative Materials Ontology**
- Defines materials, products, properties, and relationships
- Provides a structured foundation for indexing and retrieval
- Aligned with established biomedical terminology where applicable

### **2. Knowledge Graph**
- Extracted from peer-reviewed clinical studies and manufacturer documentation
- Enables transparent reasoning and source grounding
- Improves retrieval precision by replacing keyword search with ontology structure

### **3. RAG Workflow**
- Uses vector embeddings for question understanding
- Retrieves context from the ontology-indexed document set
- Feeds evidence into the LLM to generate grounded, clinically consistent answers

### **4. Streamlit UI (Prototype)**
- Simple front-end to test queries
- Displays:
  - clinician question  
  - RAG-generated answer  
  - supporting documents  
  - graph view of evidence (via Gruff / AllegroGraph)

---

## 📂 Repository Structure
├── ontology/ # Dental Restorative Materials Ontology (OWL/Turtle)
├── data/ # Curated document corpus (summaries, structured extracts)
├── ui_version_2.py # Streamlit demonstration interface
├── drmo_basic_ui2.py # Early UI prototype (for screenshots and testing)
├── rag_pipeline/ # Retrieval + embedding utilities (work in progress)
└── README.md # This file

*(Adjust after import if folder names differ.)*

---

## 🚀 Status

This repository contains a **working prototype** of the ontology-grounded RAG system used for research, evaluation, and demonstration purposes.

The code is not production-ready but demonstrates:
- feasibility  
- architecture  
- core functionality  
- integration of symbolic + neural methods  

The goal is to expand, refine, and deploy the system under the SAAKSHII initiative.

---

## 👩‍⚕️ Team

**Women-led initiative** integrating expertise in:
- clinical dentistry  
- ontology engineering  
- knowledge graphs  
- retrieval-augmented generation  
- AI safety and evaluation

Names and roles will appear in the proposal, not publicly in the repo.

---

## 🔒 API Keys and Secrets

No API keys or secrets are included in this repository.  
Any previous development keys have been revoked.

Users must provide their own environment variables for local testing.

---

## 📬 Contact

This project is part of the **AI by HER Global Impact Challenge (Healthcare Track)** and is under active development.

For inquiries, please contact the project team.

