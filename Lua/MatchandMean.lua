-- loop through ID col / folder
-- Read in fileneame col -> extract PatID and fraction
--    save file path
--    load in dicom and structure set
--    save date
--    loop through packs until date matches
--    load in dicoms and structures again
--    match to dicom scan
--    write niftis
--    calc mean signal within each mask
--    save as pack

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

-- change accordingly (if 3 digits add 0 in front) (if _new no 0's)
patID = [[0000826]]
packID = [[826]]
treatment = [[SABR]]-- [[20fractions]]-- 

packdir = [[D:\data\MRL_Prostate\]]
newpackdir = [[D:\data\prostateMR_radiomics\Packs\]]
dicomdir = [[D:\data\prostateMR_radiomics\patientData\]]..treatment..[[\]]..patID..[[\]] -- change according to patient
outputdir = [[D:\data\prostateMR_radiomics\nifti\]]..treatment..[[\]]..patID..[[\]]

scaninfo_csv = io.open([[D:\data\Aaron\ProstateMRL\Data\MRLPacks\ScanInfo\]]..patID..[[.csv]], "w", "csv")
scaninfo_csv:write("patID,MRContour,Pack,Fraction,Scan,ContourDate,ScanDate,ContourTime,ScanTime,MeanProstate,MeanShrunkProstate,MeanPsoas,MeanGlute\n")

allpacks = {}
allpacks = scandir(packdir)
patpacks = {}

-- Get just packs for patient
for p=1, #allpacks do
  if string.find(allpacks[p], packID) then
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
  
  date_match = false
  ContourFlag = false

  wm.Scan[1]:load([[DCM:]]..scan_path)
  wm.Delineation:load([[DCM:]]..delin, wm.Scan[1])
  
  scan_date = tostring(wm.Scan[1].Properties.InstanceCreationDate)
  print("Scan Date: "..scan_date)
  
  for m = 0, wm.Delineation.len do
    if string.find(wm.Delineation[m].name, "RP") then
        ContourFlag = true
        break
    end
  end  
  
  if ContourFlag == false then
    print("No RP Contour found")
    print("-------------------")
  end
    
  if ContourFlag == true then
  
    for p=1, #patpacks do
      --print("Pack: "..patpacks[p])
      loadpack(packdir..patpacks[p])
      pack_date = tostring(wm.Scan[2].Properties.InstanceCreationDate)
      
      if scan_date == pack_date then
        pack_match = patpacks[p]
        date_match = true
      end
    end
    
    if date_match == true then
      print("Pack: "..pack_match.." Date: "..scan_date)

      loadpack(packdir..pack_match)
      
      hash = string.find(pack_match, "#") -- have to change for pt in folders
      dot = string.find(pack_match, "PA")
      fraction = tonumber(string.sub(pack_match, hash+1, dot-2)) -1 -- dont need -1 for pt in folder
      
      -- check where empty scans are to load in dicom
      s = wm.Scan.len
      for t=1, s do
        if wm.Scan[t].Data.empty == true then
          e = t
          break
        end
      end

      wm.Scan[e]:load([[DCM:]]..scan_path)
      wm.Scan[e].Description = 'Original Dicom'
        
      wm.Delineation:load([[DCM:]]..delin, wm.Scan[e])

      for m = 0, wm.Delineation.len do
        if string.find(wm.Delineation[m].name, "RP") then
          RPcont = wm.Delineation[wm.Delineation[m].name]
          wm.Scan[e+1] = wm.Scan[e]:burn(RPcont, 255, true)
          wm.Scan[e+1].Description = "ProstateMask"
          break
        end
      end  
    
      wm.Scan[e+2] = wm.Scan[e+1] / 255 
      wm.Scan[e+2].Description = "ShrunkProstateMask"
      wm.Scan[e+2].Data:expand(-0.35)
      wm.Scan[e+2]:write_nifty(outputdir..dicomfolders[i]..[[\Masks\]]..patID..[[_]]..dicomfolders[i]..[[_shrunk_pros.nii]])
      
      wm.Scan[e+3]:read_nifty(outputdir..dicomfolders[i]..[[\Masks\]]..patID..[[_]]..dicomfolders[i]..[[_psoas.nii]])
      wm.Scan[e+3].Description = "PsoasMask"
      
      wm.Scan[e+4]:read_nifty(outputdir..dicomfolders[i]..[[\Masks\]]..patID..[[_]]..dicomfolders[i]..[[_glute.nii]])
      wm.Scan[e+4].Description = "GluteMask"
      
      prop_table = {}
      mean_table = {}

      for w=1, e-1 do
        wm.Scan[w].Description = wm.Scan[w].Properties.SeriesDescription
        if string.find(tostring(wm.Scan[w].Description), "T2") then -- some are T1
          
          prop_table[1] = patID
          prop_table[2] = dicomfolders[i]
          prop_table[3] = pack_match
          prop_table[4] = fraction
          prop_table[5] = w
          prop_table[6] = wm.Scan[e].Properties.InstanceCreationDate
          prop_table[7] = wm.Scan[w].Properties.InstanceCreationDate
          prop_table[8] = wm.Scan[e].Properties.InstanceCreationTime
          prop_table[9] = wm.Scan[w].Properties.InstanceCreationTime
            
          print("Matching Scan: "..w)
          -- match everything to dicom scan with contour
          selectscanstomatch(1, e, 1, 0, 0, 5, 0.0001, true, false, true, true)
          wm.MatchClipbox:fit(RPcont, 0, 4)
          startmatch()
          -- write out 
          --wm.Scan[w]:as(wm.Scan[e])
          wm.Scan[w]:write_nifty(outputdir..dicomfolders[i]..[[\Reg-Raw\]]..patID..[[_]]..dicomfolders[i]..[[_reg_img_]]..w..[[.nii]]) -- includeadjust=True
          
          -- use masks to calc mean for each mask
          for v=1, 4 do
            wm.Mask = wm.Scan[e+v]
            h = wm.Mask:histogram(wm.Scan[w], 1, 400)
            prop_table[9+v] = h:mean().value
           -- print(h:mean().value)
          end
          scaninfo_csv:write(table.concat(prop_table, ", "))
          scaninfo_csv:write("\n")
        end
      end
      
      print("--------------------------")
      savepack(newpackdir..patID..[[_]]..fraction..[[.pack]])
    end
  end  
end
scaninfo_csv:close()

print("-------Finished---------")