--[[
Data collation script
Script reads in the first image from each available fraction and the RTStruc for each patient and saves pack
cross checks against the patient list of expected patients

A McWilliam

Adapted for using RP Prostate Mask
AR
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
output = [[D:\data\prostateMR_radiomics\PatPacks\UnReg\]]

patDetails = {}
patDetails = readCSV([[D:\data\prostateMR_radiomics\DIPLproject\patients.csv]])

patTreatFolders = {}
patTreatFolders = scandir(patients)

for k = 1, #patTreatFolders do
  
  patFolders = {}
  patFolders = scandir(patients..patTreatFolders[k])
  
  for i = 1, #patFolders do
    --check ID is present in list
    patFlag = false
    for j = 1, #patDetails do
      if string.find(tostring(patFolders[i]), tostring(patDetails[j].patID)) then
        patFlag = true
        break
      end
    end
    
    if not fileexists(output..patFolders[i]..[[.pack]]) then
      if patFlag == true then
        patImages = {}
        patImages = scandir(patients..patTreatFolders[k]..[[\]]..patFolders[i])
        
        count = 1
        print("Processing patient: "..patFolders[i])
        for j = 1, #patImages do
          tmp = {}
          tmp = scandir(patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j])
          
          f = scan:new()
          f:load([[DCM:]]..patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[1])
          
          if j == 1 then
            for l=1, #tmp do
              if string.find(patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[l],'RS') then
                wm.Delineation:load([[DCM:]]..patients..patTreatFolders[k]..[[\]]..patFolders[i]..[[\]]..patImages[j]..[[\]]..tmp[l], wm.scan[1])
                break
              end
            end
          end
          
          RP_cont = false
    
          for m=1, wm.Delineation.len do
            if string.find(wm.delineation[m-1].name, 'RP') then
              scan = m-1
              RP_cont = true
            end
          end
          
          if RP_cont == true then
          
            if count>1 then
              if not (f.Properties.StudyDate == wm.Scan[count-1].Properties.StudyDate) then
                wm.Scan[count] = f
                print(j, patImages[j], wm.Scan[count].Properties.StudyDate)
                wm.Scan[count].Description = wm.Scan[count].Properties.StudyDate
                count = count + 1
              end
            else
              wm.Scan[count] = f
              print(j, patImages[j], wm.Scan[count].Properties.StudyDate)
              wm.Scan[count].Description = wm.Scan[count].Properties.StudyDate
              count = count + 1
            end
          end
        end 
        wm.Delineation:load([[DCM:]]..strucFolder..patFolders[i]..[[.dcm]], wm.Scan[1])
        -- savepack(output..patFolders[i]..[[.pack]])
        
        clear()
      end
    end
    
    
  end
  
  
end