class Utils:
    @classmethod
    def cast_to_int(cls, val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default
