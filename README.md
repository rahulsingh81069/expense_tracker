# Daily Expenses Sharing Application
# Daily Expenses Sharing API

Design and implement a backend for a daily-expenses sharing application. This
application will allow users to add expenses and split them based on three
different methods: exact amounts, percentages, and equal splits. The
application should manage user details, validate inputs, and generate
downloadable balance sheets.

## Features

- User registration with JWT authentication.
- Create and manage expenses with various split methods (equal, exact, percentage).
- Calculate individual user balances and generate a balance sheet.

## Requirements

- Python 3.x
- Django 5.1.2
- Django REST Framework
- Django Simple JWT for authentication

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```
### 2. Set Up a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```
python manage.py runserver
```

## API Endpoints:
#### Authentication

#### Register a New User - POST /api/users/

```json
{
  "username": "newuser",
  "password": "securepassword",
  "email": "newuser@example.com",
  "mobile_number": "+1234567890"
}
```

#### Obtain Token - POST /api/auth/token/

```json
{
  "username": "newuser",
  "password": "securepassword"
}
```
#### Refresh Token - POST /api/auth/token/refresh/

```json
{
  "refresh": "<refresh_token>"
}
```

### User Endpoints
#### Get User Details - GET /api/users/<user_id>/
```json
{
    "id": 1,
    "username": "rahul",
    "email": "rahul@example.com",
    "mobile_number": "+911234567890"
}
```

#### List All Users - GET /api/users/
```json
[
    {
        "id": 1,
        "username": "rahul",
        "email": "rahul@example.com",
        "mobile_number": "+911234567890"
    },
    {
        "id": 2,
        "username": "ankit",
        "email": "ankit@example.com",
        "mobile_number": "+91123091823"
    },
    {
        "id": 3,
        "username": "banke",
        "email": "banke@example.com",
        "mobile_number": "+912312312312"
    }
]
```

### Expense Endpoints
#### Create Expense - POST /api/expenses/

Exact Split Example

```json
{
  "amount": 150,
  "description": "Lassi",
  "payer": "1",
  "split_method": "exact",
  "splits": [
    {"user": 1, "amount": 50},
    {"user": 2, "amount": 25},
    {"user": 3, "amount": 25}
  ]
}

```

Equal Split Example

```json
{
  "amount": 600,
  "description": "Nightout",
  "payer": "1",
  "split_method": "equal",
  "splits": [
    {"user": 1},
    {"user": 2},
    {"user": 3}
  ]
}
```

Percentage Split Example

```json
{
  "amount": 300,
  "description": "Chicken Party",
  "payer": "1",
  "split_method": "percentage",
  "splits": [
    {"user": 1, "percentage": 50},
    {"user": 2, "percentage": 25},
    {"user": 3, "percentage": 25}
  ]
}

```

#### Retrieve User Balance - GET /api/expenses/user-balance/<user_id>/
```json
{
    "user_id": "2",
    "amount_owed_by_user": 200.0,
    "amount_owed_to_user": 0,
    "net_balance": -200.0
}
```
Retrieves the balance details for a specific user, including amounts owed by or owed to them.

#### List Expenses - GET /api/expenses/
```json
[
    {
        "id": 1,
        "amount": "600.00",
        "description": "Chicken Party",
        "payer": 1,
        "split_method": "percentage",
        "splits": [
            {
                "user": 1,
                "amount": null,
                "percentage": "50.00"
            },
            {
                "user": 2,
                "amount": null,
                "percentage": "25.00"
            },
            {
                "user": 3,
                "amount": null,
                "percentage": "25.00"
            }
        ]
    },
    {
        "id": 2,
        "amount": "100.00",
        "description": "Samosa",
        "payer": 1,
        "split_method": "exact",
        "splits": [
            {
                "user": 1,
                "amount": "50.00",
                "percentage": null
            },
            {
                "user": 2,
                "amount": "25.00",
                "percentage": null
            },
            {
                "user": 3,
                "amount": "25.00",
                "percentage": null
            }
        ]
    },
    {
        "id": 3,
        "amount": "150.00",
        "description": "Lassi",
        "payer": 1,
        "split_method": "equal",
        "splits": [
            {
                "user": 1,
                "amount": "50.00",
                "percentage": null
            },
            {
                "user": 2,
                "amount": "25.00",
                "percentage": null
            },
            {
                "user": 3,
                "amount": "25.00",
                "percentage": null
            }
        ]
    }
]
```
Retrieves all the expenses.


#### Retrieve Balance Sheet - GET /api/expenses/balance-sheet/
```json
[
    {
        "user_id": 1,
        "username": "rahul",
        "amount_owed_by_user": 0,
        "amount_owed_to_user": 400.0,
        "net_balance": 400.0,
        "total_expenses_done": 850.0
    },
    {
        "user_id": 2,
        "username": "ankit",
        "amount_owed_by_user": 200.0,
        "amount_owed_to_user": 0,
        "net_balance": -200.0,
        "total_expenses_done": 0
    },
    {
        "user_id": 3,
        "username": "banke",
        "amount_owed_by_user": 200.0,
        "amount_owed_to_user": 0,
        "net_balance": -200.0,
        "total_expenses_done": 0
    }
]
```
Returns the overall balance sheet for all users, including net balances, total expenses.

