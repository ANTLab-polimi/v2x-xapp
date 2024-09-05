
import numpy as np
from typing import List
from typing_extensions import Self
import logging

_NUMEROLOGY = 2

_RETRASMISSIONS = 1

# _ALLOWED_USED_SF_SLOTS = {
#     1:  [0, 1, 2, 3],
#     6:  [0, 1, 2, 3],
#     2:  [0, 1],
#     7:  [0, 1],
#     4:  [1, 2, 3],
#     9:  [1, 2, 3],
#     0: [],
#     3: [],
#     5: [],
#     8: []
# }

# _ALLOWED_SUBFRAMES = [1,2,4,6,7,9]

# PATTERN = np.array([2, 2, 2, 1, 0, 0, 0, 0, 0, 0])
# BITMAP = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1])

PATTERN = np.array([2, 2, 1, 0, 0, 0, 0, 0, 0, 0])
BITMAP = np.array([1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1])

class Tti:

    def __init__(self, symStart: int = 0, numSymbols: int = 0) -> None:
        self.symStart: int = symStart
        self.numSymbols: int = numSymbols

    def is_overlapping(self, otherTti: Self):
        # return max(0, min(otherTti.symStart+otherTti.numSymbols-1, self.symStart + self.numSymbols-1) - max(self.symStart, otherTti.symStart))>0
        return ((min(otherTti.symStart+otherTti.numSymbols, self.symStart + self.numSymbols) - max(self.symStart, otherTti.symStart))>0)

    def __str__(self) -> str:
        return str(self.symStart) + "," + str(self.numSymbols)

class SlotResources:
    def __init__(self, frame: int = 0, subframe: int = 0, slot: int = 0, ttis: List[Tti] = [], 
                symStart:int = 1, numSymbols:int = 0, maxSymbols = 14) -> None:
        self.frame: int = frame
        self.subframe: int = subframe
        self.slot: int = slot
        self._ttis: List[Tti] = ttis
        self.symStart: int = symStart
        self.numSymbols: int = numSymbols
        self.maxSymbols: int = maxSymbols
        self.sched_ues: List[int] = []
    
    def is_overlapping(self, tti: Tti):
        return any([_l_tti.is_overlapping(tti) for _l_tti in self._ttis])
    
    def append_tti(self, symStart: int, numSymbols: int):
        logger = logging.getLogger('')
        _tti = Tti(symStart, numSymbols)
        if self.is_overlapping(_tti):
            logger.info(f"Allocation: (f {self.frame} sf {self.subframe} s {self.slot}) {str(_tti)} is overlapping in slot {str(self)} thus we ignore")
        else:
            logger.debug(f"Allocation: (f {self.frame} sf {self.subframe} s {self.slot}) {str(_tti)} adding {numSymbols} into the total: {self.numSymbols}")
            self.numSymbols += numSymbols
            self._ttis.append(_tti)


    def __str__(self) -> str:
        return f"(f {self.frame} sf {self.subframe} s {self.slot}) " +\
                f"& ttis [{' '.join([str(_tti) for _tti in self._ttis])}] " +\
                f"& symStart {self.symStart} numsymb {self.numSymbols} max {self.maxSymbols}" +\
                f" sched ues {self.sched_ues}"
    
    def get_unassigned_symbols(self) -> int:
        # logger = logging.getLogger('')
        # logger.debug(f"Unsigned symb: {str(self)}")
        return self.maxSymbols - (self.symStart+self.numSymbols)
    
# given the slot number define if it is a sidelink slot or not
def normalize_sfnsf(frame:int, subframe: int, slot: int, numerology: int = 2):
    # get the normalized slot number
    _normalized = int(slot)
    _num_slot_per_subframe = pow(2, int(numerology))
    _normalized += int(subframe)*_num_slot_per_subframe
    _num_subframes_per_frame = 10
    _normalized += int(frame)*_num_subframes_per_frame*_num_slot_per_subframe
    return int(_normalized)

def get_phy_slot(pattern, bitmap)-> List[int]:
    _final_bitmap = []
    _bitmap_ind = 0
    # for _bitmap_ind, _bitmap_value in enumerate(_bitmap):
    # to be sure there is no loop
    if len([_elem==0  for _elem in pattern]) == 0:
        return []
    if len([_elem==1  for _elem in bitmap]) == 0:
        return []
    while(_bitmap_ind< len(bitmap)):
        for _pattern_ind, _pattern_val in enumerate(pattern):
            _bitmap_value = bitmap[_bitmap_ind]
            if _pattern_val!=0:
                _final_bitmap.append(0)
            else:
                if _bitmap_value == 1:
                    _final_bitmap.append(1)
                else:
                    _final_bitmap.append(0)
                _bitmap_ind+=1
    return _final_bitmap

def is_sidelink_slot(final_bitmap: List[int], frame:int, subframe: int, slot: int, numerology: int = 2):
    _normalize_slot = normalize_sfnsf(frame, subframe, slot, numerology)
    return final_bitmap[_normalize_slot%len(final_bitmap)]

def get_next_valid_slot(final_bitmap: List[int], frame: int, subframe: int, slot:int ):
    _is_new_subframe = False
    _is_new_frame = False
    _is_valid_slot = False  
    _next_frame = frame
    _next_subframe = subframe
    _next_slot = slot
    while(not _is_valid_slot):
        _next_slot = (_next_slot + 1)%pow(2, _NUMEROLOGY)
        _is_new_subframe = (_next_slot==0)
        _next_subframe = (_next_subframe + (1 if _is_new_subframe else 0))%10
        _is_new_frame = (_next_subframe == 0) & _is_new_subframe
        if _is_new_subframe:
            _is_new_subframe = False
        
        _next_frame = _next_frame + (1 if _is_new_frame else 0)
        if _is_new_frame:
            _is_new_frame = False 
        # stop to the next sidelink slot
        _is_valid_slot = is_sidelink_slot(final_bitmap, _next_frame, _next_subframe, _next_slot, _NUMEROLOGY)
    return _next_frame, _next_subframe, _next_slot

def get_all_sidelink_slots_in_frame(final_bitmap: List[int], frame: int) -> List[SlotResources]:
    _l_sidelink_slots:List[SlotResources] = []
    _next_frame, _next_subframe, _next_slot = frame, 0, 0
    if is_sidelink_slot(final_bitmap, _next_frame, _next_subframe, _next_slot, _NUMEROLOGY):
        _new_slot_resources = SlotResources(_next_frame, _next_subframe, _next_slot, [])
        _l_sidelink_slots.append(_new_slot_resources)
    while(_next_frame == frame):
        _next_frame, _next_subframe, _next_slot = get_next_valid_slot(final_bitmap, _next_frame, _next_subframe, _next_slot)
        if _next_frame == frame:
            _new_slot_resources = SlotResources(_next_frame, _next_subframe, _next_slot, [])
            _l_sidelink_slots.append(_new_slot_resources)
    return _l_sidelink_slots

def get_remaining_slots_for_scheduling(final_bitmap: List[int], frame: int, subframe: int, slot:int, 
                                        frame_schedule_until: int, subframe_schedule_until: int)-> int:
    _max_num_slots = _RETRASMISSIONS
    _num_slots = 0
    _next_frame, _next_subframe, _next_slot = frame, subframe, slot
    while (((_next_frame*10+_next_subframe)<(frame_schedule_until*10+subframe_schedule_until)) & (_num_slots<_max_num_slots)):
        _next_frame, _next_subframe, _next_slot = get_next_valid_slot(final_bitmap, frame, subframe, slot)
        _num_slots += 1
    return _num_slots


# def get_next_valid_slot(frame: int, subframe: int, slot:int ):
#     def _get_max_allowed_slots_in_ref_subframe(subframe):
#         try:
#             _max_allowed_slots_in_ref_subframe = max(_ALLOWED_USED_SF_SLOTS[subframe])+1
#         except ValueError:
#             # empty allowed slots
#             _max_allowed_slots_in_ref_subframe = 0
#         except KeyError:
#             # empty allowed slots
#             _max_allowed_slots_in_ref_subframe = 0
#         return _max_allowed_slots_in_ref_subframe
#     _is_new_subframe = False
#     _is_new_frame = False
#     _is_valid_slot = False
#     _transition_from_unallowed_subframe = False
#     while (not _is_valid_slot):
#         _max_allowed_slots_in_ref_subframe = _get_max_allowed_slots_in_ref_subframe(subframe)
#         if _max_allowed_slots_in_ref_subframe == 0:
#             subframe = (subframe + 1)%10
#             slot = -1 # it will add to the next iteration and start from slot = 0
#             if subframe == 0:
#                 _is_new_frame = True
#             _transition_from_unallowed_subframe = True
#         else:
#             if slot >= _max_allowed_slots_in_ref_subframe:
#                 _is_new_subframe = True
#                 slot = 0
#             else:
#                 slot = (slot+1)%_max_allowed_slots_in_ref_subframe
#                 _is_new_subframe = (slot==0) & (not _transition_from_unallowed_subframe)
#             # in case the slot goes again to 0, it means a new subframe has
#             # started, thus we add by 1
#             subframe = (subframe + (1 if _is_new_subframe else 0))%10
#             if subframe == 0:
#                 _is_new_frame = True
#             while (subframe not in _ALLOWED_SUBFRAMES):
#                 subframe = (subframe + 1)%10
#                 if subframe == 0:
#                     _is_new_frame = True
#                 slot = 0
#             try:
#                 _is_valid_slot = (subframe in _ALLOWED_SUBFRAMES) & (slot in _ALLOWED_USED_SF_SLOTS[subframe])
#             except KeyError:
#                 _is_valid_slot = False
#     # the same logic we deploy for the frame 
#     frame = frame + (1 if _is_new_frame else 0)
#     return frame, subframe, slot