from sqlalchemy.orm import Session
from models import Company_Employee_Info

# List of employee data to be inserted
employees_data = [
    {"full_name": "John Doe", "department": "Finance", "job_title": "-----------"},
    {"full_name": "Jane Smith", "department": "Finance", "job_title": "_________"},
    {"full_name": "Alice Johnson", "department": "Finance", "job_title": "-------"},

    {"full_name": "Bob Brown", "department": "Quality_Control", "job_title": "QC Agent"},
    {"full_name": "David Jones", "department": "Quality_Control", "job_title": "QC Agent"},
    {"full_name": "Jones Jones", "department": "Quality_Control", "job_title": "QC Agent"},
    {"full_name": "David Bell", "department": "Quality_Control", "job_title": "QC Agent"},
    {"full_name": "Ethan Reynolds", "department": "Quality_Control", "job_title": "QC Agent"},

    {"full_name": "Ethan Reynolds", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Olivia Carter", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Liam Mitchell", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Sophia Bennett", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Noah Harrison", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Ava Collins", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Mason Brooks", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Isabella Cooper", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Elijah Scott", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Charlotte Hayes", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "James Foster", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Amelia Richardson", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Benjamin Simmons", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Harper Edwards", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Alexander Jenkins", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Emily Griffin", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Daniel Walker", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Abigail Wright", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Henry Murphy", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Madison Price", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Samuel Russell", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Ella Rogers", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Matthew Torres", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Scarlett Peterson", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "David Powell", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Victoria Barnes", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Joseph Rivera", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Grace Patterson", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Andrew Jenkins", "department": "Repairs", "job_title": "Technician"},
    {"full_name": "Chloe Sanders", "department": "Repairs", "job_title": "Technician"},

    {"full_name": "Daniel Carter", "department": "Warehouse", "job_title": "Warehouse Agent"},
    {"full_name": "Sophia Lewis", "department": "Warehouse", "job_title": "Warehouse Agent"},
    {"full_name": "James Turner", "department": "Warehouse", "job_title": "Warehouse Agent"},
    {"full_name": "Olivia Martin", "department": "Warehouse", "job_title": "Warehouse Agent"},
    {"full_name": "Liam Adams", "department": "Warehouse", "job_title": "Warehouse Agent"},

    {"full_name": "Ethan Reynolds", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Olivia Carter", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Liam Mitchell", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Sophia Bennett", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Noah Harrison", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Ava Collins", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Mason Brooks", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Isabella Cooper", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Elijah Scott", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Charlotte Hayes", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "James Foster", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Amelia Richardson", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Benjamin Simmons", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Harper Edwards", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Alexander Jenkins", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Emily Griffin", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Daniel Walker", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Abigail Wright", "department": "Absa", "job_title": "Configuration Agent"},
    {"full_name": "Henry Murphy", "department": "Absa", "job_title": "Configuration Agent"},

    {"full_name": "William Carter", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Emma Johnson", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Michael Brown", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Sophia Williams", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Daniel Smith", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Olivia Davis", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Matthew Wilson", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Isabella Anderson", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Ethan Thomas", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Charlotte Martinez", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "James Taylor", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Amelia Hernandez", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Benjamin Moore", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Harper Jackson", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Alexander White", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Emily Harris", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Daniel Martin", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Abigail Thompson", "department": "FNB", "job_title": "Configuration Agent"},
    {"full_name": "Henry Garcia", "department": "FNB", "job_title": "Configuration Agent"},

    {"full_name": "Ethan Walker", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Olivia Carter", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Liam Mitchell", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Sophia Bennett", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Noah Harrison", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Ava Collins", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Mason Brooks", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Isabella Cooper", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Elijah Scott", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Charlotte Hayes", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "James Foster", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Amelia Richardson", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Benjamin Simmons", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Harper Edwards", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Alexander Jenkins", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Emily Griffin", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Daniel Walker", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Abigail Wright", "department": "Standard Bank", "job_title": "Configuration Agent"},
    {"full_name": "Henry Murphy", "department": "Standard Bank", "job_title": "Configuration Agent"}
]

def insert_multiple_employees(db: Session, employees_data: list):
    # Create a list of Company_Employee_Info objects from the provided data
    employees = [
        CompanyEmployeeInfo(
            full_name=emp["full_name"],
            department=emp["department"],
            job_title=emp["job_title"]
        )
        for emp in employees_data
    ]

    # Bulk insert the list of employees into the database
    db.bulk_save_objects(employees)
    db.commit()
    return employees


