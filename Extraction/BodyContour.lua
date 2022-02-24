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

dataT = [[D:\data\prostateMR_radiomics\patientData\SABR_new\]]

--output = [[D:\data\D:\data\Aaron\ProstateMRL\Extraction\patientDatainfo\]]
headerFlag = true
--file = io.output(output..[[result.txt]], 'a')

        
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)

headerFlag = true

output = [[D:\data\prostateMR_radiomics\nifti_new\new_SABR\]]

-- list patients
for i = 1, #folderPatients do
  folderVisits = {}
  folderVisits = scandir(dataT..folderPatients[i])
  
  -- list visits
  for j = 1, #folderVisits do
    folderScans = {}
    folderScans = scandir(dataT..folderPatients[i]..[["\"]]..folderVisits[j])
    
    print("Processing patient: "..folderPatients[i]..[[,  ]].." visit ".. folderVisits[j].." scan ")
    
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


      bodyMask = Scan:new()
      wm.Scan[3] = wm.Scan[1]
      bodyMask = wm.scan[3]
      bodyMask.data:treshold(5,400)

      AVS:FIELD_NORM(wm.scan[3].data, wm.scan[3].data)
      wm.mask = wm.scan[3]; 
      wm.mask = wm.mask:as(wm.scan[1])
      wm.mask.CloudDensity = 100

      finalMask = Scan:new()
      wm.scan[3] =wm.scan[3]/255
      wm.scan[3].data = wm.scan[3].data:asshort()
      wm.scan[3]:write_nifty(output..folderPatients[i]..[[\]]..folderVisits[j]..[[\]]..[[BodyMask.nii]])
      --.Scan[3] = wm.Scan[1]
      --wm.Scan[3].Data:treshold(339)
        
    
    
end
end  