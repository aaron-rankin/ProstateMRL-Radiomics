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

--output = [[D:\data\prostateMR_radiomics\patientData\nifti\new20fractions\]]
headerFlag = true
--file = io.output(output..[[result.txt]], 'a')

        
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)

headerFlag = true


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
      
    -- 
    contours = {}
    print("Number of contours: "..wm.Delineation.len)
    for m=1, wm.Delineation.len do
      contours[m] = (wm.Delineation[m-1].name)
      print(contours[m])
    end
    
    --print("Contour: "..contours[1])
    
    
    --print("Patient ID: "..wm.Scan[1].Properties.PatientID)
    --print("Age: "..wm.Scan[1].Properties.PatientAge)
    --print("Scan: "..folderVisits[j])
    --print("Number of contours: "..wm.Delineation.len)
    --for m=1, wm.Delineation.len do
     -- print(wm.Delineation[m-1].name)
    --end
    --print("Field Strength: "..wm.Scan[1].Properties.MagneticFieldStrength)
    --print("Axial slice pixels: "..wm.Scan[1].Properties.Rows..","..wm.Scan[1].Properties.Columns)
    --print("Spacing between pixels: "..wm.Scan[1].Properties.PixelSpacing)
    --print("Slice thickness: "..wm.Scan[1].Properties.SliceThickness)
    --print("Space between slices: "..wm.Scan[1].Properties.SpacingBetweenSlices)
    
    row = {wm.Scan[1].Properties.PatientID, wm.Scan[1].Properties.PatientAge, folderVisits[j], contours, wm.Delineation.len,wm.Scan[1].Properties.MagneticFieldStrength,wm.Scan[1].Properties.Rows,wm.Scan[1].Properties.Columns,wm.Scan[1].Properties.PixelSpacing,wm.Scan[1].Properties.SliceThickness,wm.Scan[1].Properties.SpacingBetweenSlices}
    --print("row contours: "..row[4])
    --contour_name:write(row.. '\n')


--savepack('**.pack')

end
end  
contour_name:close()