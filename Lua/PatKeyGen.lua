
--[[
Data collation script
Script reads in the first image from each available fraction and the RTStruc for each patient and saves pack
cross checks against the patient list of expected patients

A McWilliam
]]


function scandir(directory)
    local i, t, popen = 0, {}, io.popen
    for filename in popen('dir "'..directory..'" /o:n /b'):lines() do
        i = i + 1
        t[i] = filename
    end
    return t
end

function clear()
  for k = 1, wm.Scan.len do
    wm.Scan[k]:clear()
  end
  wm.Delineation:clear()
end

require('csv')


patients = [[D:\data\prostateMR_radiomics\patientData\]]
--strucFolder = [[D:\data\prostateMR_radiomics\DIPLproject\RTstruc\]]
outputfile = io.open([[D:\data\Aaron\ProstateMRL\Data\Extraction\PatientKey.csv]], "w", "csv")
outputfile:write("PatID,Treatment,FileDir,Scan,Date,RPCont\n")

patTreatFolders = {}
patTreatFolders = scandir(patients)

for k = 1, #patTreatFolders do
  patFolders = {}
  patFolders = scandir(patients..patTreatFolders[k])

  for i = 1, #patFolders do

      patImages = {}
      patImages = scandir(patients..patTreatFolders[k]..[[\]]..patFolders[i])
      
      count = 1
      print("Processing patient: "..patFolders[i])
      
      prop_table = {}
      
      for j = 1, #patImages do
        tmp = {}
        tmp = scandir(patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j])
        
        for l=1, #tmp do
          if string.find(patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[l],'RS') then
            wm.Scan[1]:load([[DCM:]]..patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[1])
            wm.Delineation:load([[DCM:]]..patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[l], wm.scan[1])
            struc = patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[l]
            break
          end
        end  
        RP_cont = false
        
        for m=1, wm.Delineation.len do
          if string.find(wm.delineation[m-1].name, 'RP') then
            RP_cont = true
          end
        end
        clear()
       
        
        f = scan:new()
        f:load([[DCM:]]..patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[1])
        --wm.Scan[count].Description = patImages[j]
        if count>1 then
          if not (f.Properties.StudyDate == wm.Scan[count-1].Properties.StudyDate) then
            wm.Scan[count] = f
            print(j, patImages[j], wm.Scan[count].Properties.StudyDate)
            date = wm.Scan[count].Properties.StudyDate
            wm.Scan[count].Description = wm.Scan[count].Properties.StudyDate..[[.]]..patImages[j]
            
            count = count + 1
            
            prop_table[1] = patFolders[i]
            prop_table[2] = string.gsub(patTreatFolders[k], "_new", "")
            prop_table[3] = patTreatFolders[k]
            prop_table[4] = patImages[j]
            prop_table[5] = date
            if RP_cont == true then
              prop_table[6] = "y"
            else
              prop_table[6] = "n"
            end
        
            print(table.concat(prop_table, ", "))
        --outputfile:write(table.concat(prop_table, ","))
        --outputfile:write("\n")
          end
        else
          wm.Scan[count] = f
          print(j, patImages[j], wm.Scan[count].Properties.StudyDate)
          date = wm.Scan[count].Properties.StudyDate
          wm.Scan[count].Description = wm.Scan[count].Properties.StudyDate..[[.]]..patImages[j]
          
          count = count + 1
          
          prop_table[1] = patFolders[i]
          prop_table[2] = string.gsub(patTreatFolders[k], "_new", "")
          prop_table[3] = patTreatFolders[k]
          prop_table[4] = patImages[j]
          prop_table[5] = date
          if RP_cont == true then
            prop_table[6] = "y"
          else
            prop_table[6] = "n"
          end
          
          print(table.concat(prop_table, ", "))
        --outputfile:write(table.concat(prop_table, ","))
        --outputfile:write("\n")
        end
        
        
        
        end 
        
      end
      
      clear()
    end



print("Scripted finished")
