import plotly.express as px
import pandas as pd
import streamlit as st
from datetime import datetime

current_month = datetime.now().strftime("%Y-%m")
from database import (
    create_database,
    save_transaction,
    get_transactions,
    get_total_income,
    get_total_expense,
    get_transaction_count,
    get_member_summary,
    delete_transaction,
    add_bill,
    get_bills,
    delete_bill,
    mark_bill_paid,
    get_pending_bills,
    get_month_summary,
    get_available_months,
    get_month_transaction_count,
    get_member_summary_by_month,
    get_category_summary_by_month,
    get_member_financial_summary,
    get_member_category_breakdown,
    get_member_transactions,
    add_loan,
    get_loans,
    mark_loan_paid,
    delete_loan,
    pay_loan,
    get_pending_loans
    
)

create_database()

st.set_page_config(
    page_title="PM Family Finance",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

[data-testid="stMetric"] {
    background: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

h1 {
    color: #1e293b;
}

</style>
""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "📂 Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Transaction",
        "📋 Transactions",
        "📄 Bills",
        "📊 Monthly History",
        "👨‍👩‍👧‍👦 Member Summary",
        "🏦 Loans",
        "💳 Credit Cards",
        "⚙️ Settings"
    ]
)

if menu == "🏠 Dashboard":

    from datetime import datetime

    st.title("🏠 PM Family Finance Dashboard")

    current_month = datetime.now().strftime("%Y-%m")

    income, expense = get_month_summary(
        current_month
    )

    balance = income - expense

    txn_count = get_month_transaction_count(
        current_month
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
    "💰 Income",
    f"₹{income:,.0f}"
)

    col2.metric(
    "💸 Expense",
    f"₹{expense:,.0f}"
)

    col3.metric(
    "🏦 Balance",
    f"₹{balance:,.0f}"
)

    col4.metric(
    "📋 Records",
    txn_count
)

    st.divider()

    st.subheader("🚨 Upcoming Bills")

    pending_bills = get_pending_bills()

    if pending_bills:

        for bill in pending_bills:

            st.warning(
                f"{bill[0]} | ₹{bill[1]:,.0f} | Due: {bill[2]}"
            )

    st.divider()
    st.subheader("🏦 Pending EMIs")

    pending_loans = get_pending_loans()

    if pending_loans:

        for loan in pending_loans:

            st.error(
                f"{loan[0]} | ₹{loan[1]:,.0f} | Due: {loan[2]}"
            )

    else:

        st.success(
            "No Pending Loans 🎉"
        )

    st.divider()

    member_data = get_member_summary_by_month(
        current_month
    )

    member_df = pd.DataFrame(
        member_data,
        columns=[
            "Member",
            "Expense"
        ]
    )

    st.subheader(
        "👨‍👩‍👧‍👦 Current Month Member Expenses"
    )

    st.dataframe(
        member_df,
        use_container_width=True
    )
if menu == "➕ Add Transaction":

    st.header("➕ Add Transaction")

    date = st.date_input("Date")

    member = st.selectbox(
        "Member",
        [
            "Srinivas",
            "Gani",
            "Sravani",
            "Anusha",
            "Dad",
            "Family"
        ]
    )

    txn_type = st.selectbox(
        "Type",
        [
            "Income",
            "Expense"
        ]
    )

    category = st.selectbox(
        "Category",
        [
            "Salary",
            "Business",
            "Grocery",
            "Fuel",
            "Medical",
            "Shopping",
            "Internet",
            "Electricity",
            "School Fee",
            "Travel",
            "Other"
        ]
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0
    )

    notes = st.text_area("Notes")

    if st.button("💾 Save Transaction"):

        save_transaction(
            str(date),
            member,
            txn_type,
            category,
            amount,
            notes
        )

        st.success(
            "Transaction Saved!"
        )

if menu == "📋 Transactions":

    st.header("📋 Transactions")

    transactions = get_transactions()

    if transactions:

        txn_df = pd.DataFrame(
            transactions,
            columns=[
                "ID",
                "Date",
                "Member",
                "Type",
                "Category",
                "Amount",
                "Notes"
            ]
        )

        txn_df["Amount"] = txn_df["Amount"].apply(
            lambda x: f"₹{x:,.0f}"
        )

        st.dataframe(
            txn_df[
                [
                    "Date",
                    "Member",
                    "Category",
                    "Amount"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No Transactions Found"
        )
if menu == "📄 Bills":

    st.header("📄 Bills Management")

    bill_name = st.selectbox(
        "Bill Name",
        [
            "School Fee",
            "Electricity",
            "Internet",
            "Water",
            "Gas",
            "Phone",
            "Rent",
            "Other"
        ]
    )

    bill_amount = st.number_input(
        "Amount",
        min_value=0.0,
        key="bill_amount"
    )

    due_date = st.date_input(
        "Due Date",
        key="due_date"
    )

    status = st.selectbox(
        "Status",
        [
            "Pending",
            "Paid"
        ]
    )

    if st.button("💾 Save Bill"):

        add_bill(
            bill_name,
            bill_amount,
            str(due_date),
            status
        )

        st.success(
            "Bill Saved Successfully"
        )

        st.rerun()

    st.divider()

    bills = get_bills()

    if bills:

        bill_df = pd.DataFrame(
            bills,
            columns=[
                "ID",
                "Bill",
                "Amount",
                "Due Date",
                "Status"
            ]
        )

        bill_df["Amount"] = bill_df["Amount"].apply(
            lambda x: f"₹{x:,.0f}"
        )

        st.subheader("📋 Bills List")

        st.dataframe(
            bill_df[
                [
                    "Bill",
                    "Amount",
                    "Due Date",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No Bills Found"
        )       
if menu == "📊 Monthly History":

    st.header("📊 Monthly History")

    months = get_available_months()

    if months:

        selected_month = st.selectbox(
            "📅 Select Month",
            months
        )

        income, expense = get_month_summary(
            selected_month
        )

        savings = income - expense

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "💰 Income",
            f"₹{income:,.0f}"
        )

        c2.metric(
            "💸 Expense",
            f"₹{expense:,.0f}"
        )

        c3.metric(
            "🏦 Savings",
            f"₹{savings:,.0f}"
        )

        st.divider()

        st.subheader("📂 Category Summary")

        category_data = get_category_summary_by_month(
            selected_month
        )

        category_df = pd.DataFrame(
            category_data,
            columns=[
                "Category",
                "Expense"
            ]
        )

        st.dataframe(
            category_df,
            use_container_width=True
        )

    else:

        st.info(
            "No Monthly Data Found"
        )
if menu == "👨‍👩‍👧‍👦 Member Summary":

    st.header(
        "👨‍👩‍👧‍👦 Member Summary"
    )

    months = get_available_months()

    if months:

        selected_month = st.selectbox(
            "📅 Select Month",
            months
        )

        data = get_member_financial_summary(
            selected_month
        )

        member_df = pd.DataFrame(
            data,
            columns=[
                "Member",
                "Income",
                "Expense"
            ]
        )

        member_df["Balance"] = (
            member_df["Income"]
            - member_df["Expense"]
        )

        st.dataframe(
            member_df,
            hide_index=True,
            use_container_width=True
        )
        st.divider()

        selected_member = st.selectbox(
            "👤 Select Member",
            member_df["Member"].tolist()
        )

        st.divider()

        st.subheader(
            f"📂 {selected_member} Expense Breakdown"
        )

        breakdown = get_member_category_breakdown(
            selected_month,
            selected_member
        )

        if breakdown:

            breakdown_df = pd.DataFrame(
                breakdown,
                columns=[
                    "Category",
                    "Amount"
                ]
            )

            st.dataframe(
                breakdown_df,
                hide_index=True,
                use_container_width=True
            )
            st.divider()

            st.subheader(
                f"📋 {selected_member} Transaction History"
            )

            txn_data = get_member_transactions(
                selected_month,
                selected_member
            )

            if txn_data:

                txn_df = pd.DataFrame(
                    txn_data,
                    columns=[
                        "Date",
                        "Category",
                        "Amount",
                        "Notes"
                    ]
                )

                st.dataframe(
                    txn_df,
                    hide_index=True,
                    use_container_width=True
                )

            else:

                st.info(
                    "No Transactions Found"
                )

if menu == "🏦 Loans":

    st.header("🏦 Loans")

    loan_name = st.text_input("Loan Name")

    lender = st.text_input("Bank / Finance")

    emi_amount = st.number_input(
        "EMI Amount",
        min_value=0.0
    )

    due_date = st.date_input(
        "Due Date"
    )

    notes = st.text_area("Notes")

    if st.button("💾 Save Loan"):

        add_loan(
            loan_name,
            lender,
            emi_amount,
            str(due_date),
            "Pending",
            notes
        )

        st.success(
            "Loan Added Successfully"
        )

        st.rerun()

    st.divider()

    loans = get_loans()

    if loans:

        loan_df = pd.DataFrame(
            loans,
            columns=[
                "ID",
                "Loan",
                "Lender",
                "EMI",
                "Due Date",
                "Status",
                "Notes"
            ]
        )

        loan_df["EMI"] = loan_df["EMI"].apply(
            lambda x: f"₹{x:,.0f}"
        )

        st.dataframe(
            loan_df[
                [
                    "Loan",
                    "Lender",
                    "EMI",
                    "Due Date",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No Loans Found")
if menu == "💳 Credit Cards":

    st.header("💳 Credit Cards")

    st.info("Coming Next 🚀")


if menu == "⚙️ Settings":

    st.header("⚙️ Settings")

    st.info("Coming Next 🚀")
