class TaskNode:
    def __init__(self, task_id, description):
        self.id = task_id
        self.description = description
        self.completed = False
        self.note = ""
        self.next = None


class TaskLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self._current_id = 1

    def add_task(self, description):
        new_task = TaskNode(self._current_id, description)
        self._current_id += 1

        if self.head is None:
            self.head = new_task
            self.tail = new_task
        else:
            self.tail.next = new_task
            self.tail = new_task

        self.size += 1
        return new_task

    def mark_completed(self, task_id):
        current = self.head

        while current is not None:
            if current.id == task_id:
                current.completed = True
                return True
            current = current.next

        return False

    def find_task(self, task_id):
        current = self.head

        while current is not None:
            if current.id == task_id:
                return current
            current = current.next

        return None

    def save_note(self, task_id, note):
        task = self.find_task(task_id)

        if task is None:
            return False

        task.note = note
        return True

    def build_tasks_text(self):
        if self.head is None:
            return "No tasks in the list."

        current = self.head
        output = ""

        while current is not None:
            status = "Completed" if current.completed else "Pending"
            output += f"ID: {current.id} | {current.description} | Status: {status}\n"
            current = current.next

        return output
