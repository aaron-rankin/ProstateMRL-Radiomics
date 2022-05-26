-- Read in DB

-- loop through ID col / folder
-- Read in fileneame col -> extract PatID and fraction
-- if PatID new
-- if fraction 1 
--    save file path
--    scan 1 = plan adaptation, scan 2 = verification, scan 3 = post treatment
--    load in pack and contour
--    register scan 2 and 3 to scan 1??
--    write nifti of scans and masks

-- if other fraction
--   load in pack
--   register each scan to frac 1 scan 1
--   load in contour from frac 1, shrink by 3mm at each fraction? Same for SABR and 20#
--   write nifti of registered scans and mask

-- back to top

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

-- change accordingly (if 3 digits add 0 in front)
patID = [[1089]]

packdir = [[D:\data\MRL_Prostate\]]
dicomdir = [[D:\data\prostateMR_radiomics\patientData\SABR\000]]..patID..[[\]] -- change according to patient
outputdir = [[D:\data\prostateMR_radiomics\nifti\SABR\000]]..patID..[[\]]

output_csv = io.open([[D:\data\Aaron\ProstateMRL\Data\MRLPacks\ScanInfo\]]..patID..[[.csv]], "w", "csv")
output_csv:write("patID,MRContour,Fraction,Scan,ContourDate,ScanDate,ContourTime,ScanTime\n")

allpacks = {}
allpacks = scandir(packdir)
patpacks = {}

-- Get just packs for patient
for p=1, #allpacks do
  if string.find(allpacks[p], patID) then
    table.insert(patpacks, allpacks[p])
  end
end

dicomfolders = {}
dicomfolders = scandir(dicomdir)


-- Get scan numbers so can sort per fraction
for q=1, #dicomfolders do
  dicomfolders[q] = string.gsub(dicomfolders[q], "MR", "")
  dicomfolders[q] = tonumber(dicomfolders[q])
end
table.sort(dicomfolders)
for q=1, #dicomfolders do
  dicomfolders[q] = tostring(dicomfolders[q])
  dicomfolders[q] = "MR"..dicomfolders[q]
end

-- loop through patient files
for i=1, #dicomfolders do
  print("Patient: "..patID.." Scan: "..dicomfolders[i])
  dicomscans = {}
  dicomscans = scandir(dicomdir..dicomfolders[i])

  for j=1, #dicomscans do
    -- save path to scan and delineation and load after pack because WM funny
    if string.find(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[j], 'MR') then
        scan_path = tostring(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[2])
    end
    
    if string.find(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[j], 'RS') then
        delin = tostring(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[j])
    end
    
  end
  
  wm.Scan[1]:load([[DCM:]]..scan_path)
  scan_date = tostring(wm.Scan[1].Properties.InstanceCreationDate)
  
  date_match = false

  -- ignore first pack since MR-SIM?
  -- load everything in
  for k=1, #patpacks do
    --print("Pack: "..patpacks[k])
    loadpack(packdir..patpacks[k])
    pack_date = tostring(wm.Scan[2].Properties.InstanceCreationDate)

    if scan_date == pack_date then
      --print("Match")
      pack_match = patpacks[k]
      date_match = true
      break
    end
  end
  
  if date_match == true then
    print("Match - MR: "..i.." Pack: "..pack_match.." Date: "..scan_date)
  end
  
  fraction = i-1
  
  -- check where empty scans are to load in dicom
  s = wm.Scan.len
  for t=1, s do
    if wm.Scan[t].Data.empty == true then
      e = t
      break
    end
  end

  --wm.Scan[e]:load([[DCM:]]..scan)
  --print("Dicom in: "..e)

end
output_csv:close()
print("Finished")