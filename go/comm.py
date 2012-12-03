import subprocess

p = subprocess.Popen(['cryptics'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = p.communicate("# (7) s..s.w.\n('clue', ('sub', ('sub_', 'bottomless'), ('lit', 'sea')), ('ana', ('ana_', 'stormy'), ('lit', 'sea')), ('sub', ('lit', 'waters'), ('sub_', 'surface')), ('d', 'rises_and_falls'))\n.\n")
print out.split('\n')
