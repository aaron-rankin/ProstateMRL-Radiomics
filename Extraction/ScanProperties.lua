-- Aaron Rankin 08/03/22
-- Load in dicoms and extract info from headers
-- Patient, Scan, Age, DateofScan, Manufacturer, Model, Sequence,
-- AcquisitionType, MagneticFieldStrength, PixelSpacing, Rows, Columns, Slices, 
-- SliceThickness, SpacingBetweenSlices, NumberofContours, Contours
-- write to csv

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

headerFlag = true
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)

headerFlag = true

outputfile = io.open([[D:\data\Aaron\ProstateMRL\Data\Extraction\patientDatainfo\scaninfo_20fractions.csv]], "w", "csv")
outputfile:write("Patient,Scan,Age,DateofScan,Manufacturer,Model,Sequence,AcquisitionType,MagneticFieldStrength,PixelSpacing,Rows,Columns,Slices,SliceThickness,SpacingBetweenSlices,NumberofContours,Contours \n")

properties_to_collect = {'PatientAge', 'AcquisitionDate', 'Manufacturer', 'ManufacturerModelName', 'StudyDescription', 'MRAcquisitionType', 'MagneticFieldStrength', 'PixelSpacing', 'Rows', 'Columns', 'NumberOfSlicesMR', 'SliceThickness', 'SpacingBetweenSlices'}

-- list patients
for i = 1, #folderPatients do
  folderVisits = {}
  folderVisits = scandir(dataT..folderPatients[i])
  
  -- list visits
  for j = 1, #folderVisits do
    folderScans = {}
    folderScans = scandir(dataT..folderPatients[i]..[["\"]]..folderVisits[j])
    
    print("Processing patient: "..folderPatients[i]..[[,  ]].." scan: ".. folderVisits[j])
    
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
      if string.find(wm.delineation[m-1].name, 'rostate') then
      contours[m] = (wm.Delineation[m-1].name)
      print(contours[m])
      end
    end
    
    prop_table = {}
    prop_table[1] = folderPatients[i]
    prop_table[2] = folderVisits[j]
    
     for l = 1,#properties_to_collect  do
      if type(wm.scan[1].Properties[properties_to_collect[l]]) ~= "table" then
        prop_table[l+2] = wm.scan[1].Properties[properties_to_collect[l]]
      else
        prop_table[l+2] = 'NA'
      end
    end
    
    prop_table[16] = contours.len
    prop_table[17] = table.concat(contours, " ")
    --for m = 1, wm.Delineation.len do
     -- prop_table[16+m] = wm.Delineation[m-1].name
    --end

    outputfile:write(table.concat(prop_table, ", "))
    outputfile:write("\n")
    
end
end  
outputfile:close()
print("----------Done-----------")