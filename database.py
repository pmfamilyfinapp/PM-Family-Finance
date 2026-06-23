import sqlite3
from datetime import datetime, date

DB_NAME = "family_finance.db"


def create_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            txn_date TEXT,
            member TEXT,
            txn_type TEXT,
            category TEXT,
            amount REAL,
            notes TEXT
        )
    """)
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_name TEXT,
    lender TEXT,
    emi_amount REAL,
    due_date TEXT,
    status TEXT,
    notes TEXT
)
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_name TEXT,
            amount REAL,
            due_date TEXT,
            status TEXT
        )
    """)

    conn.commit()

    conn.close()
def save_transaction(
    txn_date,
    member,
    txn_type,
    category,
    amount,
    notes
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions
        (
            txn_date,
            member,
            txn_type,
            category,
            amount,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            txn_date,
            member,
            txn_type,
            category,
            amount,
            notes
        )
    )

    conn.commit()
    conn.close()


def get_transactions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            txn_date,
            member,
            txn_type,
            category,
            amount,
            notes
        FROM transactions
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data

def get_total_income():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Income'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def get_month_summary():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Income'
        AND strftime('%Y-%m', txn_date)=strftime('%Y-%m','now')
    """)

    income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Expense'
        AND strftime('%Y-%m', txn_date)=strftime('%Y-%m','now')
    """)

    expense = cursor.fetchone()[0]

    conn.close()

    return income, expense

def get_member_summary():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            member,
            SUM(amount)
        FROM transactions
        WHERE txn_type='Expense'
        GROUP BY member
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_total_expense():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Expense'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total

def delete_transaction(transaction_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM transactions
        WHERE id=?
        """,
        (transaction_id,)
    )

    conn.commit()

    conn.close()


def add_bill(
    bill_name,
    amount,
    due_date,
    status
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO bills
        (
            bill_name,
            amount,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            bill_name,
            amount,
            due_date,
            status
        )
    )

    conn.commit()

    conn.close()


def get_bills():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            bill_name,
            amount,
            due_date,
            status
        FROM bills
        ORDER BY due_date
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data
def delete_bill(bill_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM bills
        WHERE id=?
        """,
        (bill_id,)
    )

    conn.commit()

    conn.close()
def mark_bill_paid(bill_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE bills
        SET status='Paid'
        WHERE id=?
        """,
        (bill_id,)
    )

    conn.commit()

    conn.close()
def get_pending_bills():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            bill_name,
            amount,
            due_date
        FROM bills
        WHERE status='Pending'
        ORDER BY due_date
        LIMIT 5
    """)

    data = cursor.fetchall()

    conn.close()

    return data
def get_month_summary(month):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Income'
        AND substr(txn_date,1,7)=?
    """, (month,))

    income = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Expense'
        AND substr(txn_date,1,7)=?
    """, (month,))

    expense = cursor.fetchone()[0]

    conn.close()

    return income, expense
def get_available_months():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT
            substr(txn_date,1,7)
        FROM transactions
        ORDER BY 1 DESC
    """)

    data = [row[0] for row in cursor.fetchall()]

    conn.close()

    return data
def get_available_months():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT
            substr(txn_date,1,7)
        FROM transactions
        ORDER BY 1 DESC
    """)

    months = [
        row[0]
        for row in cursor.fetchall()
    ]

    conn.close()

    return months
def get_month_transaction_count(month):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
        WHERE substr(txn_date,1,7)=?
    """, (month,))

    count = cursor.fetchone()[0]

    conn.close()

    return count
def get_member_summary_by_month(month):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            member,
            COALESCE(SUM(amount),0)
        FROM transactions
        WHERE txn_type='Expense'
        AND substr(txn_date,1,7)=?
        GROUP BY member
        ORDER BY SUM(amount) DESC
    """, (month,))

    data = cursor.fetchall()

    conn.close()

    return data

def get_category_summary_by_month(month):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM transactions
        WHERE txn_type='Expense'
        AND substr(txn_date,1,7)=?
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (month,))

    data = cursor.fetchall()

    conn.close()

    return data
def get_member_financial_summary(month):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            member,
            COALESCE(SUM(CASE
                WHEN txn_type='Income'
                THEN amount
                ELSE 0
            END),0) as income,

            COALESCE(SUM(CASE
                WHEN txn_type='Expense'
                THEN amount
                ELSE 0
            END),0) as expense

        FROM transactions

        WHERE substr(txn_date,1,7)=?

        GROUP BY member

        ORDER BY member
    """, (month,))

    data = cursor.fetchall()

    conn.close()

    return data
def get_member_category_breakdown(month, member):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category,
            SUM(amount)
        FROM transactions
        WHERE txn_type='Expense'
        AND member=?
        AND substr(txn_date,1,7)=?
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """, (member, month))

    data = cursor.fetchall()

    conn.close()

    return data
def get_member_transactions(month, member):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            txn_date,
            category,
            amount,
            notes
        FROM transactions
        WHERE member=?
        AND substr(txn_date,1,7)=?
        ORDER BY txn_date DESC
    """, (member, month))

    data = cursor.fetchall()

    conn.close()

    return data
def add_loan(
    loan_name,
    lender,
    emi_amount,
    due_date,
    status,
    notes
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO loans
        (
            loan_name,
            lender,
            emi_amount,
            due_date,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        loan_name,
        lender,
        emi_amount,
        due_date,
        status,
        notes
    ))

    conn.commit()
    conn.close()
def get_loans():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM loans
        ORDER BY due_date
    """)

    data = cursor.fetchall()

    conn.close()

    return data
def mark_loan_paid(loan_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE loans
        SET status='Paid'
        WHERE id=?
    """, (loan_id,))

    conn.commit()
    conn.close()
def delete_loan(loan_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM loans
        WHERE id=?
        """,
        (loan_id,)
    )

    conn.commit()
    conn.close()
def pay_loan(loan_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            loan_name,
            emi_amount
        FROM loans
        WHERE id=?
    """, (loan_id,))

    loan = cursor.fetchone()

    if loan:

        loan_name = loan[0]
        emi_amount = loan[1]

        cursor.execute("""
            UPDATE loans
            SET status='Paid'
            WHERE id=?
        """, (loan_id,))

        today = date.today().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO transactions
            (
                txn_date,
                member,
                txn_type,
                category,
                amount,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            today,
            "Family",
            "Expense",
            "Loan EMI",
            emi_amount,
            loan_name
        ))

    conn.commit()
    conn.close()
def get_pending_loans():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            loan_name,
            emi_amount,
            due_date
        FROM loans
        WHERE status='Pending'
        ORDER BY due_date
    """)

    data = cursor.fetchall()

    conn.close()

    return data
def get_transaction_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total