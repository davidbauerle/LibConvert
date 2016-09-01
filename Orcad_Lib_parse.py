
input_file = input('Enter INPUT File Name ')
output_file = input('Enter OUTPUT File Name ')
sym_name = input('Enter Symbol Library Name ')


fin = open(input_file, 'r')
fout = open(output_file, "w")

str2 = '"'

end = -1
start = 0
count = 0
error = False
line_count = 0

headers = []
pkg_fields = []
device_fields = []

text_line = fin.readline()  # throw away line

text_line = fin.readline()  # read headers
end = -1
start = 0
count = 0
header_count = 0
############################# Read Header line #######################
while start >= 0 :
    if count > 1000 :
        print ("********* ERROR COUNT EXCEEDED **************")
        fout.write ("\n\n********* ERROR COUNT EXCEEDED **************")
        error = True
        break
    start = text_line.find(str2, end+1)+1
    if start == 0 : break
    end = text_line.find(str2,start)
    data_p1 = (text_line[start:end])
    if data_p1 == "<null>" : data_p1 = ""
    headers.append(data_p1)
    header_count = header_count + 1
    count = count + 1
################### Find Header Locations ###############

id_filled = False
mfg_num_filled = False

   
for n in range(header_count):
    if headers[n] == 'HEADER':
        header_loc = n
    elif headers[n] == 'Part Number':
        part_num_loc = n
    elif headers[n] == 'Package':
        package_loc = n
    elif headers[n] == 'Manufacturer':
        mfg_loc = n
    elif headers[n] == 'Manufacturer Part Number': 
        if mfg_num_filled == False :
            mfg_num_loc = n   #because there are 2 mfg_num fields
            mfg_num_filled == True
    elif headers[n] == 'Description':
        des_loc = n
    elif headers[n] == 'Value':
        val_loc = n
    elif headers[n] == 'ID':
        if id_filled == False :
            id_loc = n   #because there are 2 ID fields
            id_filled == True
    elif headers[n] == 'Reference Template':
        ref_loc = n
    elif headers[n] == 'PCB Footprint':
        foot_loc = n
    elif headers[n] == 'Unit Cost':
        cost_loc = n
    elif headers[n] == 'Unit Cost Date':
        cost_date_loc = n

fout.write('Part Number')
fout.write(";")
fout.write('Part Type;')
fout.write('Manufacturer')
fout.write(";")
fout.write('Manufacturer Part Number')
fout.write(";")
fout.write("Description")
fout.write(";")
fout.write('Value')
fout.write(";")
fout.write('Rating;')
fout.write('Tolerance;')
fout.write("Schematic Symbol")
fout.write(";")
fout.write("PCB Footprint")
fout.write(";")
fout.write('Package')
fout.write(";")
fout.write('Status;')
fout.write('Comments;')
fout.write('Unit Cost')
fout.write(";")
fout.write('Unit Cost Date')
fout.write(";")
fout.write('Pspice Model;')
fout.write('Datasheet;')
fout.write("\n")


################## loop for data fields #################################
#for data2 in fin.readlines():
while error == False:
    data2 = fin.readline()
    text_line = data2.strip()
    end = -1
    start = 0
    count = 0
    pkg_fields.clear()
    device_fields.clear()

    ############## read Package Line ######################
    while start >= 0 :
        if count > 10000 :
            print ("********* Package ERROR COUNT EXCEEDED **************")
            fout.write ("\n\n********* Package ERROR COUNT EXCEEDED **************")
            error = True
            break
        start = text_line.find(str2, end+1)+1
        if start == 0 : break
        end = text_line.find(str2,start)
        data_p1 = (text_line[start:end])
        if data_p1 == "<null>" : data_p1 = ' '
        pkg_fields.append(data_p1)
        count = count + 1
    if count == 0 :
        error = True
        break
    if pkg_fields[ref_loc] != ' ' :  ## if this is not a package field skip it
    
        ############## read Device Line ######################
        
        end = -1
        start = 0
        data2 = fin.readline()  
        text_line = data2.strip()
        while start >= 0 :
            if count > 1000 :
                print ("********* Device ERROR COUNT EXCEEDED **************")
                fout.write ("\n\n********* Device ERROR COUNT EXCEEDED **************")
                print (text_line)
                error = True
                break
            start = text_line.find(str2, end+1)+1
            if start == 0 : break
            end = text_line.find(str2,start)
            data_p1 = (text_line[start:end])
            if data_p1 == "<null>" : data_p1 = ' '
            device_fields.append(data_p1)
            count = count + 1

        ################### Check Alignment ########################
        if pkg_fields[ref_loc] == ' ' :    # check if alignment is correct
            error = True
            print ("************* Error Pakage file did not line up ************")
            break

        if device_fields[part_num_loc] == '' :
#            error = True
            print ("************* Warning: No Part Number ************")
        else :
            fout.write(device_fields[part_num_loc])
        fout.write(";")
        
        fout.write(" ;")   # part type
        
        if device_fields[mfg_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[mfg_loc])
        fout.write(";")
        
        if device_fields[mfg_num_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[mfg_num_loc])
        fout.write(";")
        
        if device_fields[des_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[des_loc])
        fout.write(";")
        
        if device_fields[val_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[val_loc])
        fout.write(";")
        
        fout.write(" ;")   # rating
        
        fout.write(" ;")   # tolerance
        
        txt = '\\'
        fout.write(sym_name + txt)
        fout.write(pkg_fields[id_loc])
        fout.write(";")
        
        if pkg_fields[foot_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(pkg_fields[foot_loc])
        fout.write(";")
        
        if device_fields[package_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[package_loc])
        fout.write(";")
        
        fout.write(" ;")   # status
        
        fout.write(" ;")   # comments
        
        if device_fields[cost_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[cost_loc])
        fout.write(";")
        
        if device_fields[cost_date_loc] == '' :
            fout.write(" ")
        else : 
            fout.write(device_fields[cost_date_loc])
        fout.write(";")
            
        fout.write(" ;")   # Pspice Model
        
        fout.write(" ;")   # Datasheet
        fout.write(" \n")
        


# end of loop


    if error == True : break
#    fout.write("\n")
    line_count= line_count + 1
#    print('line count = ', line_count) 



fin.close()
fout.close()




