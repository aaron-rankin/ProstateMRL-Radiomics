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

dataT = [[D:\data\prostateMR_radiomics\patientData\SABR\]]

--output = [[D:\data\D:\data\Aaron\ProstateMRL\Extraction\patientDatainfo\]]
headerFlag = true
--file = io.output(output..[[result.txt]], 'a')

        
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)

headerFlag = true



output = io.open([[D:\data\D:\data\Aaron\ProstateMRL\Data\Extraction\patientDatainfo\scaninfo_SABR.csv]], "at", "csv")
--io.output(outputfile)
--print(io.read())
--output:write("Patient, Scan, Age, DateofScan, Manufacturer, Model, Sequence, AcquisitionType, MagneticFieldStrength, PixelSpacing, Rows, Columns, Slices, SliceThickness, SpacingBetweenSlices, Contours \n")

properties_to_collect = {'PatientAge, AcquisitionDate, Manufacturer, ManufacturerModel, StudyDescription, MRAcquisitionType, MagneticFieldStrength, PixelSpacing, Rows, Columns, NumberofSlicesMR, SliceThickness, SpacingBetweenSlices'}

-- list patients
for i = 1, #folderPatients do
  folderVisits = {}
  folderVisits = scandir(dataT..folderPatients[i])
  
  -- list visits
  for j = 1, #folderVisits do
    folderScans = {}
    folderScans = scandir(dataT..folderPatients[i]..[["\"]]..folderVisits[j])
    
    print("Processing patient: "..i..[[,  ]].." visit ".. folderVisits[j].." scan ")
    
    -- load scans and delineations
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
        if string.find(dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k], 'RS') then
          wm.Delineation:load([[DCM:]]..dataT..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..folderScans[k], wm.scan[1])
        end
      end
      
    -- Calculate number of contours and save
    contours = {}
    print("Number of contours: "..wm.Delineation.len)
    for m=1, wm.Delineation.len do
      contours[m] = (wm.Delineation[m-1].name)
      --print(contours[m])
    end
    
    prop_table = {}
    prop_table[1] = folderPatients[i]
    prop_table[2] = folderVisits[j]
  
     for l = 1,#properties_to_collect  do
      if type(wm.scan[1].Properties[properties_to_collect[l]]) ~= "table" then
        prop_table[l+1] = wm.scan[1].Properties[properties_to_collect[l]]
      else
        prop_table[l+1] = 'NA'
      end
    end
    
    y = prop_table.len
    print("Length of prop_table before: "..prop_table.len)
    for m = 1, wm.Delineation.len do
      prop_table[y+m] = wm.Delineation[m-1].name
    end
    print("Length of prop_table after: "..prop_table.len)
    print('done')
    output:write(table.concat(prop_table, ", "))
    
end
end  
output:close()