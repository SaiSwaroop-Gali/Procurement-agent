# ✈️ AI Procurement Agent for Airline Supply Chain Management

An AI-powered, human-in-the-loop procurement system for airline spare parts management. The system continuously monitors inventory levels, identifies procurement risks, enables manager approvals through Telegram, uses Gemini to interpret natural-language procurement instructions and supplier responses, automatically issues purchase orders, and updates a real-time procurement dashboard.

## 🏗️ System Architecture

![System Architecture](images/system_architecture.png)

---

## 📖 Project Overview

The idea behind this project is to develop an AI-powered Procurement Agent that can support procurement workflows in logistics-intensive industries, particularly small and medium-sized organizations that cannot afford large-scale ERP solutions such as SAP.

Rather than building another procurement platform, the goal is to create an intelligent agent that can integrate with existing business processes and assist managers with routine procurement activities while keeping humans in control of final decisions.

The system follows a Human-in-the-Loop (HITL) approach, where AI agents perform repetitive tasks such as inventory monitoring, risk assessment, order recommendation, natural-language interpretation, and purchase-order generation, while procurement managers remain responsible for approving, rejecting, or modifying procurement actions.

To demonstrate the concept, this project uses an imaginary Airline Supply Chain Management company as a case study. The aviation domain provides a realistic environment because it involves critical spare parts, strict operational requirements, multiple suppliers, and time-sensitive procurement decisions.

Due to limited infrastructure and resources, the prototype uses a static dataset that simulates an enterprise inventory database, consisting of:

- 22 different aircraft parts
- 6 different suppliers
- Business-specific reorder thresholds and stock levels

In a production environment, the same agent architecture could connect directly to real-time databases, ERP systems, or APIs and execute on scheduled intervals or event-driven triggers. For demonstration purposes, the current implementation uses command-based execution to initiate procurement runs manually.

The Procurement Agent continuously monitors inventory levels, evaluates business risks, notifies managers through Telegram, understands natural-language instructions such as "add 10 more units and make it urgent," generates professional purchase-order emails using Gemini, and coordinates supplier communication while ensuring that all final procurement decisions remain under human supervision.

The objective is not to replace procurement professionals, but to augment their capabilities by reducing manual effort, improving response times, and making intelligent procurement assistance accessible to organizations with limited resources.

---

## 📌 Problem Statement

Airline maintenance operations depend on timely availability of critical spare parts. Traditional procurement workflows often involve:

- Manual inventory monitoring
- Delayed procurement approvals
- Static reorder policies
- Slow supplier communication
- Limited visibility into procurement activities

These inefficiencies can increase operational risks and potentially lead to Aircraft on Ground (AOG) situations.

---

## 🚀 Solution

This project introduces an AI-driven procurement Agent that:

- Detects low-stock inventory items automatically
- Calculates business-aware risk levels for aviation components
- Sends approval requests through Telegram
- Supports human-in-the-loop decision making
- Understands natural-language manager instructions
- Dynamically adjusts order quantities
- Generates professional purchase-order emails using Gemini
- Sends emails automatically via Gmail
- Provides real-time analytics through Streamlit dashboards

---

## 🤖 Multi-Agent Architecture

```text
Inventory Monitoring Agent
        ↓
Risk Assessment Agent
        ↓
Telegram Approval Agent
        ↓
Manager Interpretation Agent
        ↓
Email Generation Agent
        ↓
Gmail Delivery Agent
        ↓
Streamlit Analytics Dashboard
```

---

## ✨ Features

### 📦 Inventory Monitoring

- Automatic low-stock detection
- Business-specific reorder recommendations

### ⚠️ Risk Assessment

- Critical aviation component prioritization
- High, Medium, and Low risk classification

### 👨‍💼 Human-in-the-Loop Approvals

- Telegram approval workflow
- Approve, reject, or modify procurement requests

### 🧠 AI Manager Interpretation

Managers can provide natural-language instructions such as:

- Add 10 more units
- Double the quantity
- Make it urgent
- Set quantity to 25

Gemini interprets these instructions and updates procurement decisions accordingly.

### 📧 AI Email Generation

- Professional purchase-order emails
- Dynamic urgency handling
- Automatic Gmail integration

### 📊 Dashboard Analytics

- KPI cards
- Supplier distribution
- Risk analysis
- Timeline analysis
- Search and filtering
- CSV export

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|------------|
| Programming Language | Python |
| AI Models | Gemini 2.5 Flash |
| Messaging | Telegram Bot API |
| Database | SQLite |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Data Processing | Pandas |
| Environment Management | uv |
| Email Service | Gmail SMTP |

---

## 📂 Project Structure

```text
Procurement-agent/

├── data/
│   ├── inventory.csv
│   └── procurement.db
│
├── src/
│   ├── procurement_agent.py
│   ├── telegram_listener.py
│   ├── email_agent.py
│   ├── manager_agent.py
│   ├── gmail_tool.py
│   ├── notification_tool.py
│   ├── risk_utils.py
│   ├── request_store.py
│   ├── database.py
│   ├── supplier_tool.py
│   ├── inventory_tool.py
│   ├── order_manager.py
│   └── ...
│
├── dashboard.py
├── requirements.txt
├── .env.
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
cd Procurement-agent
```

Create a virtual environment:

```bash
uv venv
```

Activate the environment:

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_app_password
```

---

## ▶️ Running the System

### Start the Telegram Listener

```bash
uv run python src/telegram_listener.py
```

### Generate Procurement Requests

```bash
uv run python src/procurement_agent.py
```

### Launch the Dashboard

```bash
uv run streamlit run dashboard.py
```

---

## 🔄 Example Workflow

```text
1. Inventory levels fall below reorder thresholds.

2. Procurement Agent generates requests.

3. Telegram bot sends approval notifications.

4. Manager approves, rejects, or modifies requests.

5. Gemini interprets manager instructions.

6. AI generates purchase-order emails.

7. Gmail sends supplier notifications.

8. Dashboard updates in real time.
```

---

## 📈 Dashboard Features

The Streamlit dashboard provides:

- Total Requests KPI
- Approved Requests KPI
- Rejected Requests KPI
- Emails Sent KPI
- High Risk KPI
- Supplier Distribution Charts
- Status Distribution Charts
- Risk Analysis Charts
- Order Timeline Analysis
- Search Functionality
- Status Filters
- Risk Filters
- CSV Export
- Request Details View
- AI Analysis Display
- Manager Instructions Display

---

## 🧪 Example Manager Instructions

The AI Manager Agent understands natural language commands such as:

```text
Add 10 more units

Double the quantity

Make it urgent

Set quantity to 25

Add another 5 units for next month's maintenance

Order 15 more and mark as highest priority
```

---

## 🚀 Future Improvements

- Docker deployment
- Google ADK integration
- MCP server support
- Supplier performance analytics
- Email history tracking
- Role-based authentication
- Cloud deployment
- Multi-user approval workflows

---

## 🎥 Demo Video

YouTube Link:

Coming Soon

---

## 📜 License

This project is developed for educational, research, and demonstration purposes.

---

## 👨‍💻 Author

Sai Swaroop Gali
