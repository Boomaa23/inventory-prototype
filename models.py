class Item:
    def __init__(self, db_id: str,
                 mfg_part_number: str, digikey_part_number: str, mouser_part_number: str,
                 quantity: int, description: str, reserved: dict,
                 created_by: str, created_epoch_millis: int):
        super().__init__()
        self.db_id = db_id
        self.mfg_part_number = mfg_part_number
        self.digikey_part_number = digikey_part_number
        self.mouser_part_number = mouser_part_number
        self.quantity = int(quantity)
        self.description = description
        self.reserved = eval(reserved) if isinstance(reserved, str) else reserved
        self.created_by = created_by
        self.created_epoch_millis = created_epoch_millis

    def get_reserved_quantity(self) -> int:
        return sum(self.reserved.values())

    def get_working_quantity(self) -> int:
        return self.quantity - self.get_reserved_quantity()

    def to_insert_str(self) -> str:
        return (f"'{self.db_id}', "
                f"'{self.mfg_part_number}', '{self.digikey_part_number}', '{self.mouser_part_number}', "
                f"'{self.quantity}', '{self.description}', '{self.reserved}', "
                f"'{self.created_by}', '{self.created_epoch_millis}'")

    def to_dict(self) -> dict:
        return {
            'db_id': self.db_id,
            'mfg_part_number': self.mfg_part_number,
            'digikey_part_number': self.digikey_part_number,
            'mouser_part_number': self.mouser_part_number,
            'quantity': self.quantity,
            'description': self.description,
            'reserved': self.reserved,
            'created_by': self.created_by,
            'created_epoch_millis': self.created_epoch_millis
        }

    def __str__(self) -> str:
        return self.to_insert_str()


BLANK_ITEM = Item(str(), str(), str(), str(), int(), str(), dict(), str(), int())
