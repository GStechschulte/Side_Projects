import markdown
import glob
import os

arr = os.listdir('/Users/wastechs/Documents/data/roam_dirty/')

read_in = 0
write_out = 0

for md in arr:

    with open('/Users/wastechs/Documents/data/roam_dirty/'+md, 'r') as f:
        try:
            data = f.read()
            html = markdown.markdown(data)
        except:
            read_in += 1
            not_read = md

    with open('/Users/wastechs/Documents/data/roam_clean/'+md, 'w') as f:
        try:
            f.write(html)
        except:
            write_out += 1
            not_wrote = md

print(read_in,'did not get parsed, and it was:')
print(write_out,'did not get parsed, and it was:')