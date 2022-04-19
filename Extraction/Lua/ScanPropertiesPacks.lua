-- Aaron Rankin 08/03/22
-- Load in dicoms and extract info from headers
-- Patient, Scan, Age, DateofScan, Manufacturer, Model, Sequence,
-- AcquisitionType, MagneticFieldStrength, PixelSpacing, Rows, Columns, Slices, 
-- SliceThickness, SpacingBetweenSlices, NumberofContours, Contours
-- write to csv

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

dataT = [[D:\data\MRL_Prostate\\]]

headerFlag = true
-- read folders
folderPacks = {}
folderPacks = scandir(dataT)

headerFlag = true

outputfile = io.open([[\\130.88.233.166\data\Aaron\ProstateMRL\Data\MRLPacks\ScanInfo\Allpacks.csv]], "w", "csv")
outputfile:write("Patient,Visit,Fraction,Scan,DateofScan,TimeofScan,PixelSpacing,Rows,Columns,Slices,SliceThickness,SpacingBetweenSlices \n")

properties_to_collect = { 'AcquisitionDate', 'AcquisitionTime', 'PixelSpacing', 'Rows', 'Columns', 'NumberOfSlicesMR', 'SliceThickness', 'SpacingBetweenSlices'}

-- list patients
for i = 1, #folderPacks do
  if string.find(dataT..folderPacks[i], '.PACK') then
    loadpack(dataT..folderPacks[i])
  
    print("Processing patient: "..folderPacks[i])
    
    patID = string.gsub(folderPacks[i], '.PACK', '')
    patID = string.gsub(patID, 'Pt','')
    hash = string.find(patID, '#')
    visit = string.sub(patID, hash+1)
    patID = string.sub(patID, 1, hash-2)
        
    prop_table = {}
    prop_table[1] = patID
    prop_table[2] = visit
    prop_table[3] = visit - 1
    
    s = wm.Scan.len
    for t=1, s do
      if wm.Scan[t].Data.empty == true then
        e = t
        break
      end
    end
    
    for s=1, e-1 do
      prop_table[4] = s
      print('Scan: '..s)
      
      for l = 1,#properties_to_collect  do
        if type(wm.scan[s].Properties[properties_to_collect[l]]) ~= "table" then
          prop_table[l+4] = wm.scan[s].Properties[properties_to_collect[l]]
        else
          prop_table[l+4] = 'NA'
        end
      end
      outputfile:write(table.concat(prop_table, ", "))
      outputfile:write("\n")
    end
    print('------------------------')
  end  



end
outputfile:close()
print("----------Done-----------")