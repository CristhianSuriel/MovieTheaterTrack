import sqlite3  # imports the sqlite library
from guests import Guests

conn = sqlite3.connect(':memory:')  # creates a memory database which resets every use
# database will be saved in a location where the script is in
c = conn.cursor()


# This creates a table in the database, run once then comment out if the database isn't memory
c.execute("""CREATE TABLE membership(
            first text, last text, email text
        )""")
# This creates a table in the database, run once then comment out
c.execute("""CREATE TABLE tickets(
            email text, ticket_number integer
        )""")


# This function will add a guests when they subscribe on a membership
def add_member(emp):
    with conn:
        c.execute("INSERT INTO membership VALUES (:first, :last, :email)",
                  {'first': emp.first, 'last': emp.last, 'email': emp.email})
        c.execute("INSERT INTO tickets VALUES (:email, :ticket_number)",
                  {'email': emp.email, 'ticket_number': emp.ticket_number})


def get_member_by_name(last_name):
    c.execute("SELECT * FROM employees WHERE last=:last",
              {'last': last_name})
    return c.fetchall()


# This function will allow members to update their email address
def update_email(emp, email):
    temp = emp.email
    with conn:
        c.execute("""UPDATE membership SET email = :email
                    WHERE first = :first and last = :last""",
                  {'first': emp.first, 'last': emp.last, 'email': email})

        c.execute("""UPDATE tickets SET email = :email
                    WHERE temp = :temp""",
                  {'email': email, 'temp': temp})


# This adds to the ticket table every new ticket purchased
def purchase_ticket(emp, ticket_number):
    with conn:
        c.execute("INSERT INTO tickets VALUES (:email, :ticket_number)",
                  {'email': emp.email, 'ticket_number': ticket_number})


# This shows all tickets bought by someone
def ticket_history(email):
    c.execute("SELECT * FROM tickets WHERE email=:email",
              {'email': email})
    return c.fetchall()


guest_1 = Guests('Jehnna', 'Smith', 'js@gmail.com', 1)
guest_2 = Guests('John', 'Doe', 'jd@gmail.com', 2)
add_member(guest_1)
add_member(guest_2)

purchase_ticket(guest_2, 3)

guest_2_lookup = ticket_history('jd@gmail.com')

for num in range(len(guest_2_lookup)):
    print(guest_2_lookup[num])

conn.close()
