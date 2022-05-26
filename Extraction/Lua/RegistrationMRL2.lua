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
packID = [[1088]]
treatment =  [[SABR]]--[[20fractions]]

packdir = [[D:\data\MRL_Prostate\]]
newpackdir = [[D:\data\prostateMR_radiomics\Packs\]]
dicomdir = [[D:\data\prostateMR_radiomics\patientData\]]..treatment..[[\000]]..patID..[[\]] -- change according to patient
outputdir = [[D:\data\prostateMR_radiomics\nifti\]]..treatment..[[\000]]..patID..[[\]]

scaninfo_csv = io.open([[D:\data\Aaron\ProstateMRL\Data\MRLPacks\ScanInfo\]]..patID..[[.csv]], "w", "csv")
scaninfo_csv:write("patID,MRContour,Fraction,Scan,ContourDate,ScanDate,ContourTime,ScanTime\n")

--meanvals_csv = io.open([[D:\data\Aaron\ProstateMRL\Data\MRLPacks\MeanValues\]]..patID..[[_WM.csv]], "w", "csv")
--meanvals_csv = io.write("patID,MRContour,Fraction,Scan,ScanDate,ContourTime,MeanProstate,MeanGlute,MeanPsoas\n")


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
  
  -- ignore first pack since MR-SIM?
  -- load everything in
  wm.Scan[1]:load([[DCM:]]..scan_path)
  scan_date = tostring(wm.Scan[1].Properties.InstanceCreationDate)
  date_match = false
  
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
    
    fraction = i-1
    
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
    wm.Scan[e+2]:write_nifty(outputdir..dicomfolders[i]..[[\000]]..patID..[[_]]..dicomfolders[i]..[[_shrunk_pros.nii]])
    
    wm.Scan[e+3]:read_nifty(outputdir..dicomfolders[i]..[[\000]]..patID..[[_]]..dicomfolders[i]..[[_psoas.nii]])
    wm.Scan[e+3].Description = "PsoasMask"
    
    wm.Scan[e+4]:read_nifty(outputdir..dicomfolders[i]..[[\000]]..patID..[[_]]..dicomfolders[i]..[[_glute.nii]])
    wm.Scan[e+4].Description = "GluteMask"
    
    prop_table = {}

    for w=1, e-1 do
      wm.Scan[w].Description = wm.Scan[w].Properties.SeriesDescription
      if string.find(tostring(wm.Scan[w].Description), "T2") then
        prop_table[1] = patID
        prop_table[2] = dicomfolders[i]
        prop_table[3] = fraction
        prop_table[4] = w
        prop_table[5] = wm.Scan[e].Properties.InstanceCreationDate
        prop_table[6] = wm.Scan[w].Properties.InstanceCreationDate
        prop_table[7] = wm.Scan[e].Properties.InstanceCreationTime
        prop_table[8] = wm.Scan[w].Properties.InstanceCreationTime
        scaninfo_csv:write(table.concat(prop_table, ", "))
        scaninfo_csv:write("\n")
          
        print("Matching Scan: "..w)
        -- match everything to dicom scan with contour
        selectscanstomatch(e, w, 1, 0, 0, 5, 0.0001, true, false, true, true)
        wm.MatchClipbox:fit(RPcont, 0, 4)
        startmatch()
        -- write out 
        wm.Scan[w]:write_nifty(outputdir..dicomfolders[i]..[[\000]]..patID..[[_]]..dicomfolders[i]..[[_reg_img_]]..w..[[.nii]])
      end
    end
    
    -- want to be only sampling prostate tissue, so shrink it

    --h = wm.mask:histogram(wm.scan[2], 255, 255)
    --h:mean().value
    print("--------------------------")
    savepack(newpackdir..patID..[[_]]..fraction..[[.pack]])
  end  
end
scaninfo_csv:close()
print("-------Finished---------")