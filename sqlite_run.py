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
def add_member(customer):
    with conn:
        c.execute("INSERT INTO membership VALUES (:first, :last, :email)",
                  {'first': customer.first, 'last': customer.last, 'email': customer.email})
        c.execute("INSERT INTO tickets VALUES (:email, :ticket_number)",
                  {'email': customer.email, 'ticket_number': customer.ticket_number})


def get_member_by_name(first_name, last_name):
    c.execute("SELECT * FROM membership WHERE last=:last and first=:first",
              {'last': last_name, 'first': first_name})
    return c.fetchall()


# This function will allow members to update their email address
def update_email(customer, email):
    temp = customer.email
    with conn:
        c.execute("""UPDATE membership SET email = :email
                    WHERE first = :first and last = :last""",
                  {'first': customer.first, 'last': customer.last, 'email': email})
        #
        # c.execute("""UPDATE tickets SET email = :email
        #             WHERE temp = :temp""",
        #           {'email': email, 'temp': temp})


# This adds to the ticket table every new ticket purchased
def purchase_ticket(customer, ticket_number):
    with conn:
        c.execute("INSERT INTO tickets VALUES (:email, :ticket_number)",
                  {'email': customer.email, 'ticket_number': ticket_number})


# This shows all tickets bought by someone
def ticket_history(email):
    c.execute("SELECT * FROM tickets WHERE email=:email",
              {'email': email})
    return c.fetchall()


# adds two guests, Jehnna and John
guest_1 = Guests('Jehnna', 'Smith', 'js@gmail.com', 1)
guest_2 = Guests('John', 'Doe', 'jd@gmail.com', 2)
add_member(guest_1)
add_member(guest_2)

# John purchases another movie ticket
purchase_ticket(guest_2, 3)
# displays John's ticket history
guest_2_history = ticket_history('jd@gmail.com')
for num in range(len(guest_2_history)):
    print(guest_2_history[num])

# prints out jehnna's membership info before and after email change
print(get_member_by_name('Jehnna', 'Smith'))
update_email(guest_1, 'djehnna@gmail.com')
print(get_member_by_name('Jehnna', 'Smith'))
# closes connection
conn.close()
