import mdl
from display import *
from matrix import *
from draw import *

frames = 1
basename = ''
knobs = []
gif = False

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
    global frames
    global basename

    for cmd in commands:
        if cmd[0] == 'frames':
            frames = cmd[1]
            print "FRAMES SET TO [%s]" % frames
        elif cmd[0] == 'basename':
            basename = cmd[1]
            print "BASENAME SET TO [%s]" % basename
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
    global knobs
    
    if frames == 1:
        print 'STATIC IMAGE'
        return
    
    knobs = [{} for f in range(frames)]

    for command in commands:        
        cmd = command[0]
        args = command[1:]
        if cmd =='vary':
            #vary [bigenator 0 24 0 1]
            
            knob_name = args[0]
            fi = int(args[1])
            ff = int(args[2])
            vi = float(args[3])
            vf = float(args[4])

            dvdf = (vf - vi)/(ff - fi)

            v_current = float(args[4])
            if ff < fi:
                print 'NEGATIVE FRAME RANGE. EXIT'
                return

            for f in range(fi, ff):
                knobs[f][knob_name] = v_current
                v_current += dvdf
                print v_current
                
    return knobs
                


def run(filename):
    """
    This function runs an mdl script
    """
    global frames
    global basename
    global knobs

    color = [255, 255, 255]
    tmp = new_matrix()
    ident( tmp )
    screen = new_screen()

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    first_pass(commands)
    second_pass(commands, frames)

    if frames > 1:
        gif = True

    for f in range(0, frames):
        tmp = new_matrix()
        ident(tmp)
        stack = [ [x[:] for x in tmp] ]
        tmp = []
        step = 0.1
        k = 1 #knob coefficient
        
        for command in commands:
            print command
            c = command[0]
            args = command[1:]


            if c == 'set_knobs':
                for sym in symbols:
                    if symbols[sym][0] == 'knob':
                        symbols[sym][1] == args[0]                        
            elif c == 'set':
                symbols[args[0]][1] = float(args[1])
            elif c == 'box':
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
                if args[3] != None: #move 0 150 0 movenator
                    k = symbols[args[3]][1]
                    
                tmp = make_translate(args[0]*k, args[1]*k, args[2]*k)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':

                if args[3] != None:
                    k = symbols[args[3]][1]
                tmp = make_scale(args[0]*k, args[1]*k, args[2]*k)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                theta = args[1] * (math.pi/180)
                if args[2] != None:
                    k = symbols[args[2]][1]
                
                if args[0] == 'x':
                    tmp = make_rotX(theta * k)
                elif args[0] == 'y':
                    tmp = make_rotY(theta * k)
                else:
                    tmp = make_rotZ(theta * k)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display' and not gif:                
                display(screen)
            elif c == 'save' and not gif:
                save_extension(screen, args[0])

        if gif:
            frame_name =  'anime/%s%03d.png' % (basename, f)
            print "SAVED FRAME %d AS [%s]" % (f, frame_name)
            for sym in symbols:
                print "KNOB: %s\tVALUE: %f" % (sym, symbols[sym][1])
            save_extension(screen, frame_name)
            clear_screen(screen)
            
