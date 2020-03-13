class Guests:
    """
    This is a small program to help keep track of AMC guests
    who also have memberships
    """
    def __init__(self, first, last, email, ticket_number):
        self.first = first
        self.last = last
        self.email = email
        self.ticket_number = ticket_number
