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
patID = [[1088]]

packdir = [[D:\data\MRL_Prostate\]]
dicomdir = [[D:\data\prostateMR_radiomics\patientData\SABR\000]]..patID..[[\]] -- change according to patient
outputdir = [[D:\data\prostateMR_radiomics\nifti\SABR\000]]..patID..[[\]]

output_csv = io.open([[D:\data\Aaron\ProstateMRL\Data\Extraction\MRL\]]..patID..[[.csv]], "w", "csv")
output_csv:write("patID, MRContour, Scan, ContourDate, ContourTime, ScanDate, ScanTime \n")

allpacks = {}
allpacks = scandir(packdir)
patpacks = {}

-- Get just packs for patient
for p=1, #allpacks do
  if string.find(allpacks[p], patID) then
    patpacks[p] = allpacks[p]
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
        scan = tostring(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[2])
    end
    
    if string.find(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[j], 'RS') then
        delin = tostring(dicomdir..[[\]]..dicomfolders[i]..[[\]]..dicomscans[j])
    end
    
  end
  
  -- ignore first pack since MR-SIM
  -- load everything in
  
  print("Pack: "..patpacks[i])
  loadpack(packdir..patpacks[i])
  s = wm.Scan.len
  for t=1, s do
    if wm.Scan[t].Data.empty == true then
      e = t
      break
    end
  end

  wm.Scan[e]:load([[DCM:]]..scan)

  prop_table = {}

  prop_table[1] = patID
  prop_table[2] = dicomfolders[i]
  prop_table[4] = wm.Scan[e].Properties.InstanceCreationDate
  prop_table[5] = wm.Scan[e].Properties.InstanceCreationTime
  
  -- check dates align
  for u=1, e-1 do
  --  print("Scan: "..u.." Date: "..wm.Scan[u].Properties.InstanceCreationDate.." Time: "..wm.Scan[u].Properties.InstanceCreationTime)
  prop_table[3] = u
  prop_table[6] = wm.Scan[u].Properties.InstanceCreationDate
  prop_table[7] = wm.Scan[u].Properties.InstanceCreationTime
  output_csv:write(table.concat(prop_table, ", "))
  output_csv:write("\n")
    
  end
  
  --print("Scan: "..e.." Date: "..wm.Scan[e].Properties.InstanceCreationDate.." Time: "..wm.Scan[e].Properties.InstanceCreationTime)


  wm.Delineation:load([[DCM:]]..delin, wm.Scan[e])

  for m = 0, wm.Delineation.len do
    --cont = wm.Delineation.name[m]
    --print(cont)
    if string.find(wm.Delineation[m].name, "RP") then
      --struc = wm.Delineation[m].name
      RPcont = wm.Delineation[wm.Delineation[m].name]
      wm.Scan[e+1] = wm.Scan[e]:burn(RPcont, 255, true)
      break
    end
  end  

  -- start matching
  for n=1, e-1 do
    print("Matching Scan: "..n)
    -- match everything to dicom scan with contour
    selectscanstomatch(e, n, 1, 0, 0, 5, 0.0001, true, false, true, true)
    wm.MatchClipbox:fit(RPcont, 0, 4)
    startmatch()
    -- write out 
    wm.Scan[s]:write_nifty(outputdir..dicomfolders[i]..[[\]]..patID..[[_]]..dicomfolders[i]..[[_reg_img_]]..n..[[_.nii]])
  end
  
  -- want to be only sampling prostate tissue, so shrink it
  wm.Scan[e+1].Data:expand(-0.3)
  wm.Scan[e+1] = wm.Scan[e+1] / 255
  wm.Scan[e+1]:write_nifty(outputdir..dicomfolders[i]..[[\]]..patID..[[_]]..dicomfolders[i]..[[_shrunk_pros.nii]])
  print("--------------------------")
    
end
output_csv:close()
print("Finished")