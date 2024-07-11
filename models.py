class Item:
    def __init__(self, db_id, mfg_part_number, quantity, description, reserved):
        self.db_id = db_id
        self.mfg_part_number = mfg_part_number
        self.quantity = int(quantity)
        self.description = description
        self.reserved = eval(reserved) if isinstance(reserved, str) else reserved

    def get_reserved_quantity(self):
        return sum(self.reserved.values())

    def get_working_quantity(self):
        return self.quantity - self.get_reserved_quantity()

    def to_insert_str(self):
        return f"'{self.db_id}', '{self.mfg_part_number}', '{self.quantity}', '{self.description}', '{self.reserved}'"

    def __str__(self):
        return self.to_insert_str()
