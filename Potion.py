class Potion:

    def __init__(self, name, heal):
        self._name = name
        self._heal = heal

    def use(self, personnage):
        personnage.set_health(
            min(
                personnage.get_health() + self._heal,
                personnage.get_max_health()
            )
        )

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name