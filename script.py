import mdl
from display import *
from matrix import *
from draw import *

frames = 1
basename = ''
knobs = []

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """
def first_pass( commands ):
    print "COMMANDS", commands
    for cmd in commands:
        if cmd[0] == 'frames':
            frames = cmd[1]
        elif cmd[0] == 'basename':
            basename = cmd[1]
        elif cmd[0] == 'vary':
            if frames == 0:
                print 'INVALID "VARY" COMMAND. EXIT'
                return
    if frames > 1:
        if basename == '':
            basename = 'def'
            print 'BASENAME UNSPECIFIED, SET TO def'
    
"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""
def second_pass( commands, num_frames ):
    if frames = 1:
        return
    knobs = [{} for f in range(frames)]
    for command in commands:        
        cmd = command[0]
        args = command[1:]
        if cmd =='vary':
            knob_name = args[0]
            frame_f = int(args[2])
            value_i = float(args[3])
            value_f = float(args[4])
            df = frame_f - frame_i

                


def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    first_pass(commands)
    second_pass(commands, frames)

    ident(tmp)
    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    tmp = []
    step = 0.1
    for command in commands:

        c = command[0]
        args = command[1:]

        if c == 'box':
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'sphere':
            add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'torus':
            add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, color)
            tmp = []
        elif c == 'move':
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'scale':
            tmp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'rotate':
            theta = args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        elif c == 'push':
            stack.append([x[:] for x in stack[-1]] )
        elif c == 'pop':
            stack.pop()
        elif c == 'display':
            display(screen)
        elif c == 'save':
            save_extension(screen, args[0])
