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

outdir = [[D:\data\prostateMR_radiomics\nifti\]]..treatment..[[\]]
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
    RP_cont = false
    
    for m=1, wm.Delineation.len do
      if string.find(wm.delineation[m-1].name, 'RP') then
        scan = m-1
        RP_cont = true
      end
    end
    
    if RP_cont == true then
      nii_file = outdir..folderPatients[i]..[[\Masks\]]..folderPatients[i]..[[_]]..folderVisits[j]..[[_shrunk_pros.nii]]
      if file_exists(nii_file) == true then
        print([[]])
      end
      if file_exists(nii_file) == false then
        RPcont = wm.Delineation[wm.Delineation[scan].name]
        wm.Scan[2] = wm.Scan[1]:burn(RPcont, 255, true)
        wm.Scan[2].Data:expand(-0.5)
        scan = string.gsub(folderVisits[j], "0","")
        wm.Scan[2]:write_nifty(outdir..folderPatients[i]..[[\]]..scan..[[\Masks\]]..folderPatients[i]..[[_]]..scan..[[_shrunk_pros_5mm.nii]])
      end
    end
  end
end
print("Finished")