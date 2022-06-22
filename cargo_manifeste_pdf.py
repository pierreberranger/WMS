from fpdf import FPDF

def cargo_manifest_pdf(id_trip):

    # recovery of the packages, containers
    trip = database.set_of_trips[id_trip]
    containers_trip = trip.set_of_containers()

    trip_weight = trip.weight()

    data = ( ("Référence des contenaires", "Description des contenaires") )
    
    for contenaire in containers_trip:
        contenaire_description = ""
        contenaire_packages = contenaire.set_of_packages()
        for package in contenaire_packages:
            contenaire_description += " " + package.description
        data += (contenaire.id, contenaire_description)
    
    # Writing
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial','B',16)
    pdf.cell(200, 20, txt = 'Cargo Manifeste', ln = 2, align = 'C')

    pdf.set_font('Arial','B',12)
    pdf.cell(200, 20, txt = f'La référence du vopdfage est : {trip.id}', ln = 2)

    pdf.set_font('Arial','B',12)
    pdf.cell(200, 20, txt = f'Poids total du voyage : {trip_weight}', ln = 2)


    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4.5
    
    lh_list = [] #list with proper line_height for each row
    use_default_height = 0 #flag

    #create lh_list of line_heights which size is equal to num rows of data
    for row in data:
        for datum in row:
            word_list = datum.split()
            number_of_words = len(word_list) #how many words
            if number_of_words>2: #names and cities formed by 2 words like Los Angeles are ok)
                use_default_height = 1
                new_line_height = pdf.font_size * (number_of_words/2) #new height change according to data 
        if not use_default_height:
            lh_list.append(line_height)
        else:
            lh_list.append(new_line_height)
            use_default_height = 0

    #create your fpdf table ..passing also max_line_height!
    for j,row in enumerate(data):
        for datum in row:
            line_height = lh_list[j] #choose right height for current row
            pdf.multi_cell(col_width, line_height, datum, border=1,align='L',ln=3, 
            max_line_height=pdf.font_size)
        pdf.ln(line_height)

    pdf.output(f'cargo_manifest{id_trip}.pdf')