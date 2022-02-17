

for i = ..

wm.scan[1]:load('')
wm.Delineation:load('')

contour_name = io.open('.txt',"w")
for i=1,wm.Delineation.len do 
  print(wm.Delineation[i].name)
  contour_name:write(wm.Delineation[i].name.. '\n')
end
contour_name:close()

--savepack('**.pack')

end