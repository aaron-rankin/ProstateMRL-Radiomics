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


packdir = [[D:\data\prostateMR_radiomics\PatPacks\UnReg\]]

allpacks = {}
allpacks = scandir(packdir)
patpacks = {}

for i = 1, #allpacks do 
  
  patID = string.gsub(allpacks[i], [[.pack]], "")
  dash = string.find(patID, "_") + 1
  patID = string.sub(patID, dash)
  print(patID)
  
  loadpack(packdir..allpacks[i])
  
  prop_table = {}
  
  s = wm.Scan.len
  for t=1, s do
    if wm.Scan[t].Data.empty == true then
      e = t - 1
      break
    end
  end
  
  print(e)
  
  for f = 1, e do
    print([[Scan: ]]..f)
    print(tostring(wm.Scan[f].Description))
  end
end