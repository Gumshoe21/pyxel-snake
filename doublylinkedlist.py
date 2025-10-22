class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head  # New node points forward to old head

        if self.head is not None:
            self.head.prev = new_node  # Old head points back to new node

        self.head = new_node  # Update the head to the new node

    # Insert a node at the end
    def insert_at_end(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node  # If list is empty, new node becomes head
            return

        temp = self.head
        while temp.next:
            temp = temp.next  # Traverse to the last node

        temp.next = new_node  # Last node points forward to new node
        new_node.prev = temp  # New node points back to last node

    # Delete a node with a specific value
    def delete(self, key):
        temp = self.head

        while temp:
            if temp.data == key:
                # Case 1: Node is head
                if temp.prev is None:
                    self.head = temp.next
                    if self.head:
                        self.head.prev = None

                # Case 2: Node is in the middle or end
                else:
                    temp.prev.next = temp.next
                    if temp.next:
                        temp.next.prev = temp.prev

                del temp  # Free memory
                return

            temp = temp.next

        print(f"Value {key} not found in list.")

    # Display the list from head to end
    def display_forward(self):
        temp = self.head
        print("Forward: ", end="")
        while temp:
            print(temp.data, end=" <-> ")
            temp = temp.next
        print("None")

    # Display the list from end to head
    def display_backward(self):
        temp = self.head
        if temp is None:
            print("List is empty.")
            return

        # Go to the last node
        while temp.next:
            temp = temp.next

        print("Backward: ", end="")
        while temp:
            print(temp.data, end=" <-> ")
            temp = temp.prev
        print("None")
