from typing import List

from evaluation.hand_calculation.tile_constants import FIVE_MAN, FIVE_PIN, \
    FIVE_SOU, RED_FIVE_MAN, RED_FIVE_PIN, RED_FIVE_SOU
from evaluation.hand_calculation.tiles import Tiles
from evaluation.hand_calculation.yaku import Yaku


class Suuankou(Yaku):
    """
    Concealed hand with for concealed koutsu/kantsu.
    """

    def __init__(self):
        super().__init__()

    def set_attributes(self):
        self.name = 'Suuankou'
        self.english = 'Four Concealed Pon'
        self.japanese = '四暗刻'
        self.chinese = '四暗刻'

        self.han_open = None
        self.han_closed = 13

        self.is_yakuman = True

    def is_condition_met(self, hand: List[List[int]], win_tile, hand_config,
                         *args):
        """
        :param hand: List of 34-arrays
        :param win_tile: Integer index
        :param hand_config: HandConfig object
        :return: Boolean
        """
        if not hand_config.is_menzen:
            return False

        def win_tile_in_item(tiles, win_tile):
            if win_tile == RED_FIVE_MAN:
                return tiles[FIVE_MAN] >= 4
            elif win_tile == RED_FIVE_PIN:
                return tiles[FIVE_PIN] >= 4
            elif win_tile == RED_FIVE_SOU:
                return tiles[FIVE_SOU] >= 4
            elif win_tile == FIVE_MAN or win_tile == FIVE_PIN \
                    or win_tile == FIVE_SOU:
                return tiles[win_tile] != 0 and tiles[win_tile] != 4
            else:
                return tiles[win_tile] != 0

        closed_koutsu_set = []

        for item in hand:
            if Tiles.is_koutsu(item) or Tiles.is_kantsu(item):
                if win_tile_in_item(item, win_tile) \
                        and not hand_config.is_tsumo:
                    continue
                closed_koutsu_set.append(item)

        return len(closed_koutsu_set) == 4
