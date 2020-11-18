class Tile:
    """
    A tile on a map. It may or may not be blocked and may or may not block sight
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # By default, if a tile blocks sight, it also blocks passage
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
