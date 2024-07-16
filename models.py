import typing


class Item:
    def __init__(self, db_id: str, mfg_part_number: str, quantity: typing.Union[int, str], description: str,
                 digikey_part_number: str, mouser_part_number: str, jlcpcb_part_number,
                 reserved: typing.Union[dict, str], created_by: str, created_epoch_millis: typing.Union[int, str]):
        super().__init__()
        self.db_id = db_id
        self.mfg_part_number = mfg_part_number
        self.quantity = int(quantity)
        self.description = description
        self.digikey_part_number = digikey_part_number
        self.mouser_part_number = mouser_part_number
        self.jlcpcb_part_number = jlcpcb_part_number
        self.reserved = eval(reserved) if isinstance(reserved, str) else reserved
        self.created_by = created_by
        self.created_epoch_millis = int(created_epoch_millis)

    def get_reserved_quantity(self) -> int:
        return sum(self.reserved.values())

    def get_working_quantity(self) -> int:
        return self.quantity - self.get_reserved_quantity()

    def to_insert_str(self) -> str:
        return (f"'{self.db_id}', '{self.mfg_part_number}', '{self.quantity}', '{self.description}', "
                f"'{self.digikey_part_number}', '{self.mouser_part_number}', '{self.jlcpcb_part_number}', "
                f"'{self.reserved}', '{self.created_by}', '{self.created_epoch_millis}'")

    def to_dict(self) -> dict[str, str]:
        return {
            'db_id': self.db_id,
            'mfg_part_number': self.mfg_part_number,
            'quantity': self.quantity,
            'description': self.description,
            'digikey_part_number': self.digikey_part_number,
            'mouser_part_number': self.mouser_part_number,
            'jlcpcb_part_number': self.jlcpcb_part_number,
            'reserved': self.reserved,
            'created_by': self.created_by,
            'created_epoch_millis': self.created_epoch_millis
        }

    def __str__(self) -> str:
        return self.to_insert_str()


class User:
    def __init__(self, db_id: str, name: str, authmask: str):
        self.db_id = db_id
        self.name = name
        self.authmask = int(authmask)

    def to_insert_str(self) -> str:
        return f"'{self.db_id}', '{self.name}', '{self.authmask}'"

    def to_dict(self) -> dict[str, str]:
        return {
            'db_id': self.db_id,
            'name': self.name,
            'authmask': self.authmask
        }


BLANK_ITEM = Item(*[str('0')]*10)
BLANK_USER = User(*[str('0')]*3)
