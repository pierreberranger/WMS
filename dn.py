import enum
import collections

LAYUP_RATE = 0.05
CALL_RATES = {'8':(0.14,0.25), '12C': (0.24,0.35)}
GARBAGE_RATE = 90

class Call(enum.IntEnum):
	IN=0
	OUT=1

DNInfo = collections.namedtuple("DNInfo", "ship_name ship_flag ship_type ship_loa ship_bm ship_msd call_type call_in call_out from_port to_port")

def q_626(days_in_port: int, ship_volume: int):
	"""
	Stationnement
	"""
	return (days_in_port-2)*ship_volume*LAYUP_RATE

def q_622(ship_type: str, ship_volume:int, call:int):
	return ship_volume*RATES[ship_type][call]

def q_634(days_in_port: int):
	return GARBAGE_RATE*(days_in_port // 7 + 1)

def dn_pdf(dn_info: DNInfo):
	pass
