
--[[
Registers patient images across fractions to first fraction image

A McWilliam
]]


function scandir(directory)
    local i, t, popen = 0, {}, io.popen
    for filename in popen('dir "'..directory..'" /o:n /b'):lines() do
        i = i + 1
        t[i] = filename
    end
    return t
end

packFolder = [[D:\data\prostateMR_radiomics\PatPacks\UnReg\]]
output = [[D:\data\prostateMR_radiomics\PatPacks\Reg\]]

patPacks = {}
patPacks = scandir(packFolder)

for i = 1, #patPacks do
  if not fileexists(output..patPacks[i]) then 
    print("Processing: "..string.gsub(patPacks[i], [[.pack]], ""))
    loadpack(packFolder..patPacks[i])
    
    -- find prostate
    prostateFlag = ''
    for j = 1, wm.Delineation.len do
      if string.find(wm.Delineation[j-1].name, "RP") then
        prostateFlag = (j-1)
        break
      end
    end
    
    wm.MatchClipbox:fit(wm.Delineation[prostateFlag], 1, 3)
    
    for j = 2, wm.Scan.len do
      if not wm.Scan[j].Data.empty then
        print("Scan: "..j)
        selectscanstomatch(1, j, 1, 6, 0, 10, 0.0001, true, false, true, false)
        startmatch() 
      end
    end
    
    savepack(output..patPacks[i])
  end
end

print("Script finished")