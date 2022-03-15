click_dir = [[D:\data\prostateMR_radiomics\MuscleClicks\20fractions\]]
--pat_dir = [[D:\data\prostateMR_radiomics\patientData\20fractions\]]
output_dir = [[D:\\data\\prostateMR_radiomics\\MuscleClicks\\20fractions_nifti\\]]

function scandir(directory)
  local i, t, popen = 0, {}, io.popen
  for filename in popen('dir "'..directory..'" /o:n /b'):lines() do
    i = i + 1
    t[i] = string.gsub(filename, '.xdr', '')
  end
  return t
end

folderClicks = {}
folderClicks = scandir(click_dir)

for i=1, #folderClicks do
  print(click_dir..folderClicks[i]..".xdr")
  wm.Scan[1]:read_xdr(click_dir..folderClicks[i]..".xdr")
  
  wm.Scan[2] = wm.Scan[1]/255
  --wm.scan[2].data:toshort()
  wm.Scan[2]:write_nifty(output_dir..folderClicks[i]..".nii")
end