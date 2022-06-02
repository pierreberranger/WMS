import enum
import collections
from itertools import product
from math import ceil
import datetime

import click
from fpdf import FPDF
from pdfrw import PageMerge, PdfWriter, PdfReader

PORTS = ["FRSML","JESTH"]
BERTHS = ["DT1", "DT2", "V1"]

LAYUP_RATE = 0.0214
CALL_RATES = {'8':(0.1494,0.1494), '12C': (0.3577,0.2949)}
GARBAGE_RATE = 94.77

RATIO_REDUCTIONS = [(2/15,0.1),
(1/10,0.3),
(1/20,0.5),
(1/40,0.6),
(1/100,0.7),
(1/250,0.8),
(1/500,0.95)
]

FREQUENCY_REDUCTIONS = [
(4,0.05),
(6,0.1),
(9,0.15),
(15,0.5),
(25,0.6),
(50,0.7)
]

SHIP_TAX_THRESHOLD = 0.01
SHIP_TAX_MINIMUM = 10.41

_DATE_FORMATS = click.DateTime(["%d%m%y","%d%m%Y", "%d/%m/%Y","%d/%m/%y"])

class Call(enum.IntEnum):
    IN=0
    OUT=1

LOCATIONS = {
    "ship_name": (20,32),
    "ship_flag": (80,29),
    "ship_type": (80,37),
    "from_port": (40,52),
    "to_port": (88,52),
    "shipping_company_address_1":(60,94),
    "shipping_company_address_2":(60,98),
    "shipping_company_address_3":(60,102),
    "customs_office":(130,20),
    "port":(130,27),
    "call_date_in": (130, 38),
    "call_date_out": (170,38),
    "berth": (160,45),
    "pax": (160,52),
    "conventional_cargo": (145,82),
    "total_cargo":(145,98),
    "ship_tax_threshold": (120,111),
    "ship_tax_minimum":(120,115),
    "ship_loa": (15,131),
    "ship_bm": (45,131),
    "ship_msd": (75,131),
    "ship_volume": (110,131),
    "ship_tax_base_rate":(135,131),
    "goods_to_volume_ratio": (65,144),
    "goods_to_volume_reduction": (85, 144),
    "calls_this_year": (15,157),
    "calls_this_year_reduction": (35, 157),
    "garbage_tax_threshold": (120, 189),
    "garbage_tax_minimum": (120,193),
    "garbage_tax_value": (90, 205),
    "gross_ship_tax": (182,125),
    "non_cumulative_reductions":(182, 132),
    "total_reductions": (182,150),
    "net_ship_tax": (182,158),
    "perceived_ship_tax": (182, 170),
    "net_garbage_tax": (182, 195),
    "perceived_garbage_tax": (182, 206),
    "summary_label_1":(20,266),
    "summary_label_2":(20,272),
    "summary_label_3": (20,277),
    "summary_value_1": (35,266),
    "summary_value_2": (35,272),
    "summary_value_3": (35,277),
    "total_perceived": (35,288),
    "signing_person": (145, 263),
    "signing_person_title": (145, 270),
    "signing_location": (132, 286),
    "signing_date": (175, 286)
}



southern_liner_base_vals = {
    "ship_name": "Southern Liner",
    "ship_flag": "Panama",
    "ship_type": "12C",
    "shipping_company_address_1":"Nostos Alpha",
    "shipping_company_address_2":"7 Quai Duguay-Trouin",
    "shipping_company_address_3":"35400 Saint-Malo",
    "customs_office":"Saint-Malo",
    "port":"Saint-Malo",
    "berth": "DT2",
    "pax": "0 pax",
    "ship_loa": "55.9 m",
    "ship_bm": "12.1 m",
    "ship_msd": "4.0 m",
    "ship_volume": "2706 m3",
    "summary_label_1":"Q622",
    "summary_label_2":"Q626",
    "summary_label_3": "Q634",
    "signing_person": "Pierre Vennin",
    "signing_person_title": "Directeur Général",
    "signing_location": "Saint-Malo",
}

DNInfo = collections.namedtuple("DNInfo", "ship_name ship_flag ship_type ship_loa ship_bm ship_msd call_type call_in call_out from_port to_port")

def layup_tax(days_in_port: int, ship_volume: int):
    return (days_in_port-2)*ship_volume*LAYUP_RATE

def gross_ship_tax(ship_type: str, ship_volume:int, call:int):
    return ship_volume*CALL_RATES[ship_type.upper()][call]

def net_ship_tax(calls_this_year,ratio,ship_type, ship_volume, call):
    reduction = max(frequency_reduction(calls_this_year), ratio_reduction(ratio))
    gst = gross_ship_tax(ship_type, ship_volume, call)
    return (1-reduction)*gst

def frequency_reduction(calls_this_year):
    for n,v in reversed(FREQUENCY_REDUCTIONS):
        if calls_this_year > n:
            return v
    return 0

def ratio_reduction(ratio: float):
    for r,v in reversed(RATIO_REDUCTIONS):
        if ratio <= r:
            return v
    return 0

def garbage_tax(days_in_port: int):
    return GARBAGE_RATE*ceil(days_in_port / 7)

def dn_pdf_content(data):
    fpdf = FPDF()
    fpdf.add_page()
    fpdf.set_font("courier", size=10)
    fpdf.set_line_width(1)
    if data['call_type'] == Call.IN:
        fpdf.line(133,10,155,10)
    else:
        fpdf.line(107,10,130,10) #out
    
    for key, (x,y) in LOCATIONS.items():
        fpdf.text(x, y, str(data.get(key,'')))
    
    reader = PdfReader(fdata=bytes(fpdf.output()))
    return reader.pages[0]

def fill_pdf(content, base_fname, out_fname):
    trailer = PdfReader(base_fname)
    PageMerge(trailer.pages[0]).add(content, prepend=False).render()
    PdfWriter(out_fname, trailer=trailer).write()

def days_in_port(date_in,date_out):
    return (date_out - date_in).days + 1

def layup_days(in_date, out_date):
    if in_date > out_date:
        raise ValueError
    return max((out_date - in_date).days - 2,0)

def southern_liner():
    
    # Gather User Information
    try:
        click.echo("Déclaration sur les Navires (DN)")
        click.echo("================================")
        click.echo("MV SOUTHERN LINER, IMO 8112689")
        date_in = click.prompt("Date d'arrivée à Saint-Malo", type=_DATE_FORMATS)
        date_out = click.prompt("Date de départ de Saint-Malo", type=_DATE_FORMATS)
        tonnage_in = click.prompt("Tonnage transporté à l'entrée (kg)", type=int)
        tonnage_out = click.prompt("Tonnage transporté à la sortie (kg)", type=int)
        berth = click.prompt("Quai/Poste d'accueil", type=click.Choice(BERTHS), default="DT2")
        calls_this_year = click.prompt("Nombre de touchés cette année",type=int)
    except click.exceptions.Abort:
        click.echo("\nBye...")
        return
    # DN Entrée
    added_vals = {"call_type": 0,
        "from_port": "JESTH",
        "to_port": "FRSML",
        "call_date_in": date_in.strftime("%d-%m-%Y"),
        "call_date_out": date_out.strftime("%d-%m-%Y"),
        "ship_tax_base_rate": CALL_RATES["12C"][0],
        "conventional_cargo": f"{tonnage_in} kg",
        "total_cargo": f"{tonnage_in} kg",
        "berth": berth }
    if tonnage_in > 0:
        ratio = tonnage_in/1000/2706
        added_vals["gross_ship_tax"] = gross_ship_tax("12C",2706,0)
        added_vals["goods_to_volume_ratio"] = "{0:.4f}".format(ratio)
        added_vals["goods_to_volume_reduction"] = "-{0:.0f}%".format(100*ratio_reduction(ratio))
        added_vals["calls_this_year"] = calls_this_year
        added_vals["calls_this_year_reduction"] = "-{0:.0f}%".format(100*frequency_reduction(calls_this_year))
        added_vals["total_reductions"] = "-{0:.0f}%".format(100*max(ratio_reduction(ratio),frequency_reduction(calls_this_year)))
        nst = net_ship_tax(calls_this_year,ratio,"12C",2706,0)
        added_vals["perceived_ship_tax"] = "{0:.2f}".format(nst)
        added_vals["summary_value_1"] = "{0:.2f}".format(nst)
    else:
        added_vals["total_perceived"] = 0

    fill_pdf(dn_pdf_content(southern_liner_base_vals | added_vals),"base_files/DN_base.pdf", f"output/DN_ENTREE_{date_in.strftime('%d%m%y')}.pdf")
    
    # DN Sortie
    added_vals = {"call_type": 1,
    "from_port": "FRSML",
    "to_port": "JESTH",
    "call_date_in": date_in.strftime("%d-%m-%Y"),
    "call_date_out": date_out.strftime("%d-%m-%Y"),
    "ship_tax_base_rate": CALL_RATES["12C"][1],
    "conventional_cargo": f"{tonnage_out} kg",
    "total_cargo": f"{tonnage_out} kg",
    "berth": berth }

    ratio = tonnage_out/1000/2706

    added_vals["gross_ship_tax"] = "{0:.2f}".format(gross_ship_tax("12C",2706,1))
    added_vals["goods_to_volume_ratio"] = "{0:.4f}".format(ratio)
    added_vals["goods_to_volume_reduction"] = "-{0:.0f}%".format(100*ratio_reduction(ratio))
    added_vals["calls_this_year"] = calls_this_year
    added_vals["calls_this_year_reduction"] = "-{0:.0f}%".format(100*frequency_reduction(calls_this_year))
    added_vals["total_reductions"] = "-{0:.0f}%".format(100*max(ratio_reduction(ratio),frequency_reduction(calls_this_year)))
    nst = net_ship_tax(calls_this_year,ratio,"12C",2706,1)
    added_vals["perceived_ship_tax"] = "{0:.2f}".format(nst)
    added_vals["summary_value_1"] = "{0:.2f}".format(nst)

    gt = garbage_tax(days_in_port(date_in, date_out))
    added_vals["perceived_garbage_tax"] = "{0:.2f}".format(gt)
    added_vals["summary_value_3"] = "{0:.2f}".format(gt)

    lt = layup_tax(days_in_port(date_in, date_out), 2706)
    added_vals["summary_value_2"] = "{0:.2f}".format(lt)

    added_vals["total_perceived"] = "{0:.2f}".format(nst + gt + lt)
    fill_pdf(dn_pdf_content(southern_liner_base_vals | added_vals),"base_files/DN_base.pdf", f"output/DN_SORTIE_{date_out.strftime('%d%m%y')}.pdf")

if __name__ == '__main__':
    southern_liner()