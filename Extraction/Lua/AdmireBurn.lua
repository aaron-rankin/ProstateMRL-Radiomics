-- Aaron Rankin 08/03/22 
-- Loads in dicom files and delineations 
-- Saves as niftis

function scandir(directory)
    local i, t, popen = 0, {}, io.popen
    for filename in popen('dir "'..directory..'" /o:n /b'):lines() do
        i = i + 1
        t[i] = filename
    end
    return t
end

function folderExists(strFolderName)
	local fileHandle, strError = io.open(strFolderName.."\\*.*","r")
	if fileHandle ~= nil then
		io.close(fileHandle)
		return true
	else
		if string.match(strError,"No such file or directory") then
			return false
		else
			return true
		end
	end
end

function clear()
  for i = 1, wm.scan.len do
    if not scan[i].data.empty then
      wm.scan[i]:clear()
    end
  end
  wm.Delineation:clear()
end

dataT = [[D:\data\prostateMR_radiomics\patientData\20fractions\]]
dataAdm = [[D:\data\prostateMR_radiomics\AdmireContours\20fractions\]]

output = [[D:\data\prostateMR_radiomics\patientData\nifti\]]
headerFlag = true
--file = io.output(output..[[result.txt]], 'a')

        
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)
folderPatientsAdm = scandir(dataAdm)

--load data
-- list patient folders
for i = 1, #folderPatients do
  folderVisits = {}
  folderVisits = scandir(dataT..folderPatients[i])
  folderVisitsAdm = {}
  folderVisitsAdm = scandir(dataAdm..folderPatientsAdm[i])
  --list visits
  for j = 1, #folderVisits do
    folderScans = {}
    folderScans = scandir(dataT..folderPatients[i]..[[\]]..folderVisits[j])
    AdmContours = scandir(dataAdm..folderPatientsAdm[i]..[[\]]..folderVisitsAdm[j])
    --list scans
    --for k = 1, #folderScans do
     -- PtImages = {}
     -- PtImages = scandir(dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k])
      
      --check both sets of observers are present
      print("Processing patient "..i..[[,  ]]..folderPatients[i].." visit "..folderVisits[j].." scan ")
      
      -- look for MR and structures and load
      MRflag = false
      for k = 1, #folderScans do
        if MRflag == false then
          if string.find(dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k], 'MR') then
            wm.scan[1]:load([[DCM:]]..dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k])
            MRflag = true
          end
        end
      end
      for k = 1, #folderScans do
        if string.find(dataAdm..folderPatientsAdm[i]..[[\]]..folderVisitsAdm[j], 'AdmCont') then
          wm.Delineation:load([[DCM:]]..dataAdm..folderPatientsAdm[i]..[[\]]..folderVisitsAdm[j], wm.scan[1])-- wm.scan[1])
        end
      end
      
      -- find contours and burn
      flagContour1 = false; flagContour2 = false;
      
      wm.scan[2]:clear()
      for m = 1, wm.delineation.len do
        if string.find(wm.delineation[m-1].name, 'rostate') then
          struc_1B = wm.Delineation[wm.delineation[m-1].name]
          wm.scan[2] = wm.scan[1]:burn(struc_1B, 255, true)
          flagContour1 = true
          break
        end
      end
      --if flagContour1 == false then
        --print("Patient "..i..[[,  ]]..folderPatients[i].." visit "..folderVisits[j].." scan "..folderScans[k]..[[AD contour not found]])
      --end
      
         -- save files for radiomics analysis
        saveNii = true
        if saveNii == true then
          radiomicsOutput = [[D:\data\prostateMR_radiomics\nifti\20fractions\]]
          --os.execute('mkdir '..radiomicsOutput..folderPatients[i])
          --os.execute('mkdir '..radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j])
          
          -- need binary masks 1 and 0
          wm.scan[2] = wm.scan[2]/255;  
          
         -- wm.scan[1]:write_nifty(radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_image.nii]])
          
          wm.scan[2]:write_nifty(radiomicsOutput..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_Admire.nii]])
         
         
         ProcessMessages()
         collectgarbage()
        end
      
    
    end
  end


io.close(file)  

print("Script finished")