import sys
from typing import List, Dict, Any

class BorrowLimitExceeded(Exception):
    pass

class Member:
    def __init__(self, member_id: str, name: str, membership_type: str):
        # Validate constraints
        if len(member_id) > 10:
            raise ValueError("Member ID must contain at most 10 characters.")
        if len(name) > 50:
            raise ValueError("Name must contain at most 50 characters.")
        
        self._member_id: str = member_id
        self._name: str = name
        self._membership_type: str = membership_type
        self.__borrowed_books: int = 0


    def get_borrowed_books(self) -> int:
        return self.__borrowed_books

    def set_borrowed_books(self, count: int) -> None:
        if count < 0:
            raise ValueError("Number of borrowed books cannot be negative.")
        self.__borrowed_books = count

    def borrow_book(self, count: int) -> None:
        raise NotImplementedError("Subclasses must implement borrow_book method.")

    def return_book(self, count: int) -> None:

        if count < 0:
            raise ValueError("Books to return must be a non-negative integer.")
        
        current_borrowed = self.get_borrowed_books()
        if count > current_borrowed:
            raise ValueError("A member cannot return more books than they have currently borrowed.")
        
        self.set_borrowed_books(current_borrowed - count)

    def display_details(self) -> None:
        print(f"{'Member ID'.ljust(17)}: {self._member_id}")
        print(f"{'Name'.ljust(17)}: {self._name}")
        print(f"{'Membership Type'.ljust(17)}: {self._membership_type}")
        print(f"{'Books Borrowed'.ljust(17)}: {self.get_borrowed_books()}")


class RegularMember(Member):
    MAX_LIMIT = 3

    def __init__(self, member_id: str, name: str):
        super().__init__(member_id, name, "Regular")

    def borrow_book(self, count: int) -> None:
        if count < 0:
            raise ValueError("Books to borrow must be a non-negative integer.")
        
        if self.get_borrowed_books() + count > self.MAX_LIMIT:
            raise BorrowLimitExceeded(f"Regular Member can borrow a maximum of {self.MAX_LIMIT} books.")
        
        self.set_borrowed_books(self.get_borrowed_books() + count)

    def display_details(self) -> None:
        super().display_details()
        remaining_limit = self.MAX_LIMIT - self.get_borrowed_books()
        print(f"{'Remaining Limit'.ljust(17)}: {remaining_limit}")


class PremiumMember(Member):
    MAX_LIMIT = 10

    def __init__(self, member_id: str, name: str):
        super().__init__(member_id, name, "Premium")

    def borrow_book(self, count: int) -> None:
        if count < 0:
            raise ValueError("Books to borrow must be a non-negative integer.")
        
        if self.get_borrowed_books() + count > self.MAX_LIMIT:
            raise BorrowLimitExceeded(f"Premium Member can borrow a maximum of {self.MAX_LIMIT} books.")
        
        self.set_borrowed_books(self.get_borrowed_books() + count)

    def display_details(self) -> None:
        super().display_details()
        remaining_limit = self.MAX_LIMIT - self.get_borrowed_books()
        print(f"{'Remaining Limit'.ljust(17)}: {remaining_limit}")


def parse_input_stream() -> List[Dict[str, Any]]:
    """Memory-efficient parsing engine to clean and collect variable structural inputs."""
    lines = [line.strip() for line in sys.stdin if line.strip()]
    if not lines:
        return []

    parsed_members = []
    current_member: Dict[str, Any] = {}

    for line in lines[1:]:
        if line.startswith("Member "):
            if current_member:
                parsed_members.append(current_member)
                current_member = {}
            continue
        
        if ":" in line:
            key, val = map(str.strip, line.split(":", 1))
            current_member[key] = val

    if current_member:
        parsed_members.append(current_member)

    return parsed_members


def main():
    raw_data = parse_input_stream()
    
    unique_ids = set()
    members_list: List[Member] = []
    
    for data in raw_data:
        m_id = data.get("Member ID")
        name = data.get("Name")
        m_type = data.get("Membership Type (Regular/Premium)")
        
        if m_id in unique_ids:
            raise ValueError(f"Constraint Violation: Member ID {m_id} must be unique.")
        unique_ids.add(m_id)

        if m_type == "Regular":
            member_obj = RegularMember(m_id, name)
        elif m_type == "Premium":
            member_obj = PremiumMember(m_id, name)
        else:
            continue

        member_obj.pending_borrow = int(data.get("Books to Borrow", 0))
        member_obj.pending_return = int(data.get("Books to Return", 0))
        
        members_list.append(member_obj)

    print("------MEMBER DETAILS ------\n")
    for index, member in enumerate(members_list):
        try:
            if member.pending_borrow > 0:
                member.borrow_book(member.pending_borrow)
            if member.pending_return > 0:
                member.return_book(member.pending_return)
            
            member.display_details()
            
        except BorrowLimitExceeded as e:
            print(f"BorrowLimitExceeded: {e}")
            
        if index < len(members_list) - 1:
            print("\n-------------------\n")


if __name__ == "__main__":
    main()