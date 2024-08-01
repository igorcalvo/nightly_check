class Variable:
    def __init__(
        self,
        enabled: bool,
        category: str,
        name: str,
        question: str,
        message: str,
        condition: str,
        frequency: str,
    ):
        self.enabled = enabled
        self.category = category
        self.name = name
        self.question = question
        self.message = message
        self.condition = condition
        self.frequency = frequency
