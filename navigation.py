class Navigation:
    def __init__(self, history):
        self.history = history

    def previous(self):
        return self.history.previous()

    def next(self):
        return self.history.next()

    def jump_to(self, step):
        return self.history.jump_to(step)

    def current(self):
        if self.history.current_index >= 0:
            return self.history.get(self.history.current_index)
        return None
