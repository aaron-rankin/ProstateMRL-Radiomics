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

function file_exists(name)
   local f=io.open(name,"r")
   if f~=nil then io.close(f) return true else return false end
end
    
    
  treatment = [[20fractions_new]]

dataT = [[D:\data\prostateMR_radiomics\patientData\]]..treatment..[[\]]

headerFlag = true
-- read folders
folderPatients = {}
folderPatients = scandir(dataT)

headerFlag = true

nii_dir = [[D:\data\prostateMR_radiomics\nifti\]]..treatment..[[\]]
-- list patients
for i = 1, #folderPatients do
  folderVisits = {}
  folderVisits = scandir(nii_dir..folderPatients[i])
  
  -- list visits
  for j = 1, #folderVisits do
    folderScans = {}
    folderScans = scandir(nii_dir..folderPatients[i]..[["\"]]..folderVisits[j])
    
    print("Processing patient: "..folderPatients[i]..[[,  ]].." scan: ".. folderVisits[j])
    
    
    limbus_mask = (nii_dir..folderPatients[i]..[[\]]..folderVisits[j]..[[\Masks\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_Limbus.nii]])
    --print(limbus_mask)
    --nii_file = outdir..folderPatients[i]..[[\Masks\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_shrunk_pros.nii]]
      if file_exists(limbus_mask) == true then
          wm.Scan[1]:read_nifty(limbus_mask)
          wm.Scan[2] = wm.Scan[1]
          wm.Scan[2].Data:expand(-0.35)
          wm.Scan[2]:write_nifty(nii_dir..folderPatients[i]..[[\]]..folderVisits[j]..[[\Masks\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_Limbus_shrunk.nii]])
      end
  end
end

print([[-------- Done --------]])