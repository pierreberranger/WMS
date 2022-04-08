import enum
import collections
from itertools import product

from fpdf import FPDF
from pdfrw import PageMerge, PdfWriter, PdfReader

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

def dn_pdf_content():
    fpdf = FPDF()
    fpdf.add_page()
    fpdf.set_font("courier", size=6)
    for x,y in product(range(0,200,30),range(0,400,10)):
        fpdf.text(x, y, f"{x} {y}")
    reader = PdfReader(fdata=bytes(fpdf.output()))
    return reader.pages[0]

def fill_pdf(content, base_fname, out_fname):
    trailer = PdfReader(base_fname)
    PageMerge(trailer.pages[0]).add(content, prepend=False).render()
    PdfWriter(out_fname, trailer=trailer).write()

fill_pdf(dn_pdf_content(),'DN_base.pdf', 'DN_grid.pdf')