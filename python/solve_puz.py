import puzpy.puz as puz
from solve_clue import CrypticClueSolver
import sys
import readline


def rlinput(prompt, prefill=''):
    readline.set_startup_hook(lambda: readline.insert_text(prefill))
    try:
        return raw_input(prompt)
    finally:
        readline.set_startup_hook()

with CrypticClueSolver() as solver:
    fname = sys.argv[1]
    p = puz.read(fname)

    while True:
        p.print_clue_state()
        action = raw_input("Action? [q]uit [s]ave or enter a clue ID (e.g. 12a): ")
        if action == "q":
            break
        elif action == "s":
            p.save(fname)
        else:
            clue = p.find_clue(action.strip())
            if clue is not None:
                while True:
                    print "Current clue:", p.encode_clue_for_solver(clue)
                    action = raw_input("Clue action? [s]olve [b]ack [g]uess [e]dit: ")
                    if action == "s":
                        solver.setup(p.encode_clue_for_solver(clue))
                        try:
                            answers = solver.run()
                            for i in range(min(40, len(answers))):
                                print i, answers[i]
                            action = raw_input("Enter a number to select that answer, or leave blank to cancel: ")
                            if action.strip() != "":
                                try:
                                    choice = int(action)
                                except ValueError:
                                    break
                                p.set_clue_fill(clue, answers[choice].answer)
                                break
                        except KeyboardInterrupt:
                            solver.reset()
                    elif action == "b":
                        break
                    elif action == "g":
                        ans = raw_input("Proposed answer: ")
                        p.set_clue_fill(clue, ans)
                        break
                    elif action == "e":
                        clue['clue'] = rlinput("Edited clue: ", clue['clue'])
        p.save(fname)
