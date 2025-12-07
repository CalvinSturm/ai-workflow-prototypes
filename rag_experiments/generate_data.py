from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_pdf(filename, title, content_lines):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, title)
    
    # Body
    c.setFont("Helvetica", 12)
    y_position = height - 100
    
    for line in content_lines:
        c.drawString(72, y_position, line)
        y_position -= 20
        # Simple page break logic
        if y_position < 72:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = height - 72
            
    c.save()
    print(f"✅ Generated: {filename}")

# --- DATASET 1: HR Policy (Rules & Dates) ---
hr_content = [
    "Effective Date: January 1, 2025",
    "Subject: Remote Work & Expense Policy",
    "",
    "1. Hybrid Work Model:",
    "Employees are required to be in the office on Tuesdays and Thursdays.",
    "Monday, Wednesday, and Friday are designated remote work days.",
    "",
    "2. Home Office Stipend:",
    "Full-time employees are eligible for a one-time stipend of $500.",
    "This must be used for monitors, chairs, or desks.",
    "Receipts must be submitted to expense@corp.com by Q1 end.",
    "",
    "3. Coffee Allowance:",
    "The company does NOT reimburse for daily coffee runs.",
    "However, client meetings at coffee shops are reimbursable up to $15.",
]

# --- DATASET 2: Project Zeus (Technical Specs) ---
tech_content = [
    "Project Code: ZEUS-X1",
    "Classification: TOP SECRET",
    "Lead Engineer: Dr. Elena Vance",
    "",
    "System Architecture:",
    "The Zeus platform runs on a Kubernetes cluster named 'Olympus'.",
    "It utilizes three microservices:",
    " - Hermes: The message broker (Kafka)",
    " - Apollo: The frontend UI (React)",
    " - Hades: The persistent storage layer (PostgreSQL)",
    "",
    "Deployment Protocol:",
    "Deployments occur every Tuesday at 02:00 UTC.",
    "In case of failure, run the rollback script: /bin/undo_zeus.sh",
    "The API key for the staging environment is: 888-KEY-ALPHA-9",
]

# --- DATASET 3: Financials (Numbers & Tables) ---
finance_content = [
    "Q3 Financial Outlook - 2024",
    "Prepared by: Joshua from Finance",
    "",
    "Revenue Breakdown:",
    "- Enterprise Subscriptions: $4.5M (Up 12% YoY)",
    "- Professional Services: $1.2M (Down 5% YoY)",
    "- Licensing: $800k (Flat)",
    "",
    "Major Expenses:",
    "- Server Costs (AWS): $450k",
    "- Employee Salaries: $2.1M",
    "- The 'Team Retreat' in Cabo: $120k (Under Review)",
    "",
    "Forecast:",
    "We are projecting to hit profitability by Q4 2025.",
    "Cash runway is currently 18 months.",
]

if __name__ == "__main__":
    print("--- 🏭 Generating Synthetic Corporate Data ---")
    create_pdf("HR_Policy.pdf", "Corporate Policy Handbook 2025", hr_content)
    create_pdf("Project_Zeus.pdf", "Project Zeus Technical Specifications", tech_content)
    create_pdf("Q3_Financials.pdf", "Q3 2024 Financial Report", finance_content)
    print("--- 🏁 Done. Files ready for RAG. ---")