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


patID = [[1088]]

packdir = [[D:\data\prostateMR_radiomics\Packs\]]

allpacks = {}
allpacks = scandir(packdir)
patpacks = {}

-- Get just packs for patient
for p=1, #allpacks do
  if string.find(allpacks[p], patID) then
    table.insert(patpacks, allpacks[p])
  end
end

for i=1, #patpacks do
  loadpack(packdir..patpacks[i])
  
  s = wm.Scan.len
  for t=1, s do
    if wm.Scan[t].Data.empty == true then
      e = t - 5
      break
    end
  end
  
  for j=1, e do
      print(tostring(wm.Scan[j].Description))
      for k=1, 4 do
        wm.Mask = wm.Scan[e+k]
        h = wm.Mask:histogram(wm.Scan[j], 1, 400)
        print(h:mean().value)
      end
  end
  
  
end
