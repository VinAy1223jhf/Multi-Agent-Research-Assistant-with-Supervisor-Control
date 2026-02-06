# 🧠 Agentic Research Assistant

> 🚀 A supervisor-controlled multi-agent AI system built with LangGraph for automated research and concise summarization.

---

## ✨ What is this project?

**Agentic Research Assistant** is a multi-agent AI workflow where different AI agents collaborate to complete a research task in a structured and controlled manner.

Instead of a single chatbot, this system uses **multiple specialized agents** coordinated by a **Supervisor agent** that decides *who should work next* and *when the task is complete*.

This project focuses on **agent orchestration and workflow design**, not just prompt engineering.

---

## 🧩 How it Works (Graphical view)

<img width="721" height="726" alt="image" src="https://github.com/user-attachments/assets/979ea55a-80e7-4d6d-8808-02c0b34e73ca" />



- 🕵️ **Researcher Agent** → gathers information using web search
- ✍️ **Analysis Agent** → analysis thhe findings of research agent  
- ✍️ **Writer Agent** → summarizes findings clearly  
- 🧠 **Supervisor Agent** → controls execution flow and task completion  

---

## 🔑 Key Features

✅ Multi-agent collaboration using LangGraph  
✅ Supervisor-based workflow control  
✅ Tool-augmented research (web search)  
✅ State-driven execution and message memory  
✅ Clean separation of agent responsibilities  

---

## 🛠 Tech Stack

- **Python**
- **LangGraph**
- **LangChain Core**
- **Groq LLMs (LLaMA models)**
- **Tavily Search API**

---

## 📌 Why this project?

Most AI demos stop at chatbots.

This project explores:
- How **real agentic systems are structured**
- How agents **coordinate, loop, and stop**
- How supervisors manage **complex workflows**

It serves as a **foundation project** for building more advanced agentic AI systems.

---

## ⚠️ Disclaimer

This project is built for **learning and architectural understanding**.  
The focus is on **agent workflows**, not production deployment.

---

⭐ If you found this useful, feel free to star the repo!

