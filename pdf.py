from fpdf import FPDF
from service_layer_display import incoming_dates_list, database

def planning_incoming() :
    """ 
    Make a pdf describing the dates of the arrival of dropoffs 
    by chronological order
    """

    pdf = FPDF()
    
    # Adding a page
    pdf.add_page()
    pdf.set_margins(10, 10, 10)

    # Title
    pdf.set_font("Arial", size = 15)
    pdf.cell(100, 10, txt = "Planning of the arrivals of droppoffs", ln = 1, align ='C', border=1)

    # Subtitle
    pdf.set_font("Arial", size = 13, style="B")
    pdf.cell(200, 20, txt = "Date : id, sender, description", ln = 2)
    incoming_dates = incoming_dates_list()
    for date in incoming_dates :
        for dropoff in database.set_of_dropoffs :
            
            if dropoff.arrival_date == date :
                pdf.set_font("Arial", size = 9) 
                pdf.cell(200, 10, txt = f"{date} : {dropoff.id}, {dropoff.sender}, {dropoff.description}", ln = 2)

    # save the pdf
    pdf.output("output/planning.pdf")
