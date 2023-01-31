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

dir_pack = [[D:\data\prostateMR_radiomics\PatPacks\UnReg\]]
dir_limbus = [[D:\data\prostateMR_radiomics\PatPacks\LimbusSegmentation\]]
dir_nifti = [[D:\data\prostateMR_radiomics\PatPacks\LimbusMasks\]]

packs = scandir(dir_pack)

for p=1, #packs do
  x = string.find(packs[p], "_%d+")
  treatment = string.sub(packs[p],1,x-1)
  patID = string.sub(packs[p], x+1, string.len(packs[p]) - 5)
  
  print(treatment..[[ ]]..patID)
  
  loadpack(dir_pack..packs[p])
  
  s = wm.Scan.len
  for t=1, s do
    if  wm.Scan[t].Data.empty == true then
      num_scans = t - 1
      break
    end
  end
  for t=1, num_scans do
    if wm.Scan[t].Data.empty == false then
      name_scan = tostring(wm.Scan[t].Description)
      MR_scan = string.sub(name_scan, string.len(name_scan) - 3, string.len(name_scan))
      
      name_limbus = treatment..[[_]]..patID..[[_]]..t..[[_limbus]]
      
      AVS:READ_XDR(wm.Delineation.Lut, dir_limbus..name_limbus..[[.dwl]])
      AVS:READ_XDR(wm.Delineation.Index, dir_limbus..name_limbus..[[.dwi]])
      AVS:READ_XDR(wm.Delineation.Dots, dir_limbus..name_limbus..[[.dwp]])
      
      if string.find(MR_scan, "0") == 3 then
        MR_scan = string.gsub(MR_scan, "0", "")
      end
      name_output = treatment..[[_]]..patID..[[_]]..t..[[_Limbus]]
      
      wm.Scan[num_scans + 1] = wm.Scan[t]:burn(wm.Delineation["Prostate"], 255, true)
      wm.Scan[num_scans + 1]:write_nifty(dir_nifti..name_output..[[.nii]])
      
    end
  end

  
  
  
end