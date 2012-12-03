import subprocess

p = subprocess.Popen(['cryptics'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p.stdin.write("# (7) s..s.w.\n")
print "wrote config"
print p.stdout.readline()
print p.stdout.readline()
p.stdin.write("('clue', ('sub', ('sub_', 'bottomless'), ('lit', 'sea')), ('ana', ('ana_', 'stormy'), ('lit', 'sea')), ('sub', ('lit', 'waters'), ('sub_', 'surface')), ('d', 'rises_and_falls'))\n")
print "wrote clue"
print p.stdout.readline()
p.stdin.write(".\n")
print "wrote ."
p.wait()
