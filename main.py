import OpenGL, sys, random, time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
from cgkit.all import *
from particle import particle
from numerical_integration import *

k, rest_len, damp = 0.3, 0.2, 0.3
particle_radius = 90
nt = [["EulerIntegration",0],
      ["VerletIntegration",1]
      ]
gravity = (0,0.25,0)
windows_h, windows_w = 512, 512
fps = 0.0
frames = 0
previousTime = 0.0
t = 0.0
onscreen_fps = 0.0
timeclock = time.time()
prev_time = time.time()
count_time = 0.0
sum_time_for_calc = 0.0
time_display1=time_display2=time_display3 = 0.0

timeInterval = 0.0
f = open("./fps_analysis.txt","w")
f.write("frames count_time fps time_for_calc sum_time_for_calc currentTime previousTime timeInterval time_display1 time_display2 time_display3\n")
currentTime = previousTime = 0.0

fix_framerate = False
FRAME_PER_SECOND = 60
SKIP_TICKS = 1000/FRAME_PER_SECOND

mouse_button = [GLUT_UP, GLUT_UP, GLUT_UP, GLUT_UP, GLUT_UP]

#init particle
#ball_1 = particle(mass=1,pos=(0,0,0))
#ball_2 = particle(mass=1,pos=(3,-10,0))



def initCloth():
    global particles,neibors
    particles = []
    neibors = [[1,0], [0,1]]
    for i in range(0,10):
        particles.append(particle(mass=1,pos=(random.random()*20-10,i*-10,0),nt=nt))
        
      
#    for i in range(10):
#        particles.append([])
#        for j in range(10):
#            particles[i].append(particle(mass=1,pos=(j,0,i),nt=nt))
#            
#    for i in range(10):
#        particles[i][0].pin = True

    particles[0].pin = True

def screenDisplay(data):
    x = 20
    y = 20
    for d in data:
        text = str(d[0])+' : '+str(d[1])
        writeMessage(text,x=x,y=y,stroke=False)
        y += 20


def accumulateForce(p1, p2, k, rest_len, kd, gravtiy):
    u = p1.pos - p2.pos
    d = u.length() - rest_len
    un = u.normalize()

    #f_spring = -k * d * un
    f_spring = (-k * d * un)
    f_external = ((p2.mass+p1.mass)/2) * vec3(gravity)
    f_damper = kd * p2.vel
    F = f_spring + f_external + f_damper
    p1.F = F
    p2.F = -F

def integrate(p, dt):
    if not p.pin:
        p = NumericalIntegration(p.nt, p, dt)

def myIdle():
    global prev_time, dt, neibors, count_time, fps, t, time_for_calc, sum_time_for_calc, f
    cur_time = time.time()
    #dt = round(cur_time - prev_time,3)
    
    #dt = cur_time-prev_time
    dt = 0.03
    #dt = random.random()*0.01
    #prev_time = cur_time
    #print(dt)

    time_for_calc = time.time()
    for i in range(len(particles)-1):
        #particles[i].update_spring(particles[i+1], k, rest_len, damp, gravity)
        
        accumulateForce(particles[i], particles[i+1], k, rest_len, damp, gravity)
        #add gravity
        #particles[i].F += gravity
        #print(particles[i].accel)
        #particles[i].update_location(dt)
        #particles[i+1].update_location(dt)
        integrate(particles[i], dt)
        integrate(particles[i+1], dt)
#    for i in range(10):
#        for j in range(10):
#            for neiborP in neibors:
#                print(neiborP)
#                try:
#                    n = particles[i+neiborP[0]][j+neiborP[1]]
#                    particles[i][j].update_spring(n, k, rest_len, damp, gravity)
#                    n.update_location(dt)
##                    particles[i][j].update_spring(particles[i+1][j], k, rest_len, damp, gravity)
##                    particles[i][j].update_spring(particles[i][j+1], k, rest_len, damp, gravity)                
##                    
##                    particles[i][j+1].update_location(dt)
##                    particles[i+1][j].update_location(dt)
    
                    
#                    
#                except:
#                    continue
            
     
    time_for_calc = time.time()-time_for_calc   
    sum_time_for_calc += time_for_calc    
    fps = calculateFPS()
    #print("fps: {0}".format(type(fps)))

    count_time += dt
    
    #debug
    text = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}".format(frames,count_time,fps,time_for_calc,sum_time_for_calc,currentTime,previousTime,timeInterval,time_display1,time_display2,time_display3)
    
    #f.write(text+"\n")
    #print(text)
    
    
    glutPostRedisplay()
    
    
#    time_thisframe = time.time()-cur_time
#    fps = 1/(( time_thisframe*0.9) + (time_lastframe*0.1))
#    #print("frame:{0} curT:{1} t:{2} fps:{3} : {4} {5} {6}".format(frames,count_time,t,round(fps,2),cur_time,time.time(),time.time()-cur_time))
#    #print(1/fps)
#    count_time += dt     
#    
#    time_lastframe = time_thisframe
#    print(glutGet(GLUT_ELAPSED_TIME))
    #time.sleep(0.01)
    
#    if frames==0:
#        t = time.time()
#    frames += 1
#    if frames >= 5:
#        fps = (frames/ (time.time()-t))
#        #onscreen_fps = fps
#        frames = 0
#        print("")
#        #print("fps = {0}").format(fps)    

def calculateFPS():
    global previousTime, frames, fps, sum_time_for_calc, timeInterval, currentTime, previousTime
    frames +=1
    currentTime = glutGet(GLUT_ELAPSED_TIME)
    #Calculate time passed
    timeInterval = currentTime - previousTime
    
    if timeInterval > 1000:
        #print("frames:{0}".format(frames))
        #print("timeInterval:{0}".format(timeInterval))
        fps = frames / (timeInterval / 1000.0)
        previousTime = currentTime
        
        frames = 0
        sum_time_for_calc = 0.0
        #print("fps: {0}".format(type(fps)))
    return fps

def GetOGLPos(x,y):
    
    modelviewMat = glGetDoublev(GL_MODELVIEW_MATRIX)
    projectionMat = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)
    
    winX = float(x)
    winY = float(viewport[3]) - float(y)
    #glReadPixels( x, int(winY), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT, &winZ )
    winZ = glReadPixels(x, int(winY), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    #gluUnProject( winX, winY, winZ, modelview, projection, viewport, &posX, &posY, &posZ)
    pos = gluUnProject( winX, winY, winZ, modelviewMat, projectionMat, viewport)
    
    return vec3(pos)

def myDisplay():
    global onscreen_fps, timeclock, next_game_tick
    global time_display1, time_display2, time_display3
    
    time_display1 = time.time()
    

    
    #####PART1
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    time_display1 = time.time()-time_display1
    
    
    
    if time.time()-timeclock >= 1:
        onscreen_fps = fps
        timeclock = time.time()
        
    time_display2 = time.time()
#    try:
    screenDisplay([['FPS',round(onscreen_fps,2)]
                   #['K',k] , ['Rest_len',rest_len] 
                   #['Damp',damp], 
                   #['DeltaT',dt],
                   #['NT',[n[0] for n in nt if n[1]==1][0]]
                   #['ball_2@accel',particles[1].vel],
                   #['ball_2@accel',particles[1].accel]
                   ])
#    except:
#        print("onscreen_fps")
#        print(onscreen_fps)
#        print(type(onscreen_fps))
#        print("fps")
#        print(fps)
#        print(type(fps))
    #writeMessage("FPS : {0}".format(str(round(onscreen_fps,2))), stroke=False, win_w=windows_w, win_h=windows_h)
    time_display2 = time.time()-time_display2
    
    time_display3 = time.time()  
    
    glPushMatrix()
    gluLookAt(15, 15, 15, 0, 0, 0, 0, 1, 0)
    
    time_display3 =time.time()-time_display3
    
    ##########
    
    
    #####PART2
    
    axis_size = 5
    #draw center point
    glPointSize(5)
    glColor3f(1,0,0)
    glBegin(GL_POINTS)
    glVertex3f(0,0,0)
    glEnd()  
    
    #draw x-axis
    glPointSize(1)
    glColor3f(1,0,0)
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(axis_size,0,0)
    glEnd()
    #draw y-axis
    glColor3f(0,1,0)
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(0,axis_size,0)
    glEnd() 
    #draw z-axis
    glColor3f(0,0,1)
    glBegin(GL_LINES)
    glVertex3f(0,0,0)
    glVertex3f(0,0,axis_size)
    glEnd()     
    
    
    
    #########
#    for i in range(len(particles)):
#        for j in range(len(particles[i])):
#            currentP = particles[i][j]
#            glPointSize(2)
#            glBegin(GL_POINTS)
#            glColor3f(1,0,1)
#            glVertex3f(*currentP.pos)
#            glEnd()
#            
#            try:
#                nextP = particles[i][j+1]
#                glBegin(GL_LINES)
#                glVertex3f(*currentP.pos)
#                glVertex3f(*nextP.pos)
#                glEnd()
#                
#                nextP = particles[i+1][j]
#                glBegin(GL_LINES)
#                glVertex3f(*currentP.pos)
#                glVertex3f(*nextP.pos)
#                glEnd()                
#            except:
#                pass
        
      
    #####PART3

    for i in range(len(particles)):
        glPointSize(particles[i].mass*5)
        glBegin(GL_POINTS)
        glColor3f(*particles[i].col)
        glVertex3f(*particles[i].pos)
        glEnd()
#        
    for i in range(len(particles)-1):
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(*particles[i].pos)
        glVertex3f(*particles[i+1].pos)
        glEnd()
        
    
    #########
#        
#    glColor3f(1,0,1)
#    glBegin(GL_LINES)
#    for p in particles:
#        try:
#            v = p.vel.normalize()
#        except:
#            v = vec3(0,0,0)
#        glVertex3f(*p.pos)
#        glVertex3f(*(p.pos+v*1))
#    glEnd()   
#    #ball1
#    glPointSize(ball_1.mass*10)
#    glBegin(GL_POINTS)
#    glColor3f(1,1,1)
#    glVertex3f(*ball_1.pos)
#    glEnd()
#    
#    #ball2
#    glPointSize(ball_2.mass*10)
#    glBegin(GL_POINTS)
#    glColor3f(1,1,1)
#    glVertex3f(*ball_2.pos)
#    glEnd()   
#      
#    
#    #line ball1 >> ball2
#    glBegin(GL_LINES)
#    glVertex3f(*ball_1.pos)
#    glVertex3f(*ball_2.pos) 
#    glEnd() 
        
#    for i in range(1000):
#        glPointSize(random.random()*5)
#        glColor3f(random.random(),random.random(),random.random())
#        glBegin(GL_POINTS)
#        glVertex3f(random.random()*5-2.5,random.random()*5-2.5,0)
#        glEnd()    

    glPopMatrix()
    
    if fix_framerate:
        next_game_tick += SKIP_TICKS
        sleep_time = next_game_tick - glutGet(GLUT_ELAPSED_TIME)
        if sleep_time >= 0:
            time.sleep(sleep_time/1000.0)    
    
    glutSwapBuffers() 
    

    
#    if frames==0:
#        t = time.time()
#    frames += 1
#    if frames >= 5:
#        fps = (frames/ (time.time()-t))
#        #onscreen_fps = fps
#        frames = 0
#        #print("fps = {0}").format(fps)

    #time_for_display = time.time()-time_for_display
        
def myMotion(x, y):
    global rot_x, rot_y, mouse_button, mouse_sensitive, mouse_x, mouse_y
    if mouse_button[GLUT_LEFT_BUTTON] == GLUT_DOWN:
        pass
#        click_pos = GetOGLPos(x,y)
#        nearest_point = getNearestPoint(click_pos,particle_radius)
#        if nearest_point != None:
#            nearest_point.pin = True


        #rot_y += ((x - mouse_x) * mouse_sensitive)
        #rot_x += ((y - mouse_y) * mouse_sensitive)
        #print("rot_x:{0} rot_y:{1}".format(rot_x, rot_y))

    #mouse_x = x
    #mouse_y = y  

def getNearestPoint(cp, r):
    nearest_dist = 99999
    nearest_point = None
    for p in particles:
        dist = (cp - p.pos).length()
        if dist < nearest_dist:
            nearest_dist = dist
            nearest_point = p
          
    #print(nearest_dist)  
    if nearest_dist<=r:
        return nearest_point
    else:
        return None

def myMouse(button, state, x, y):
    mouse_button[button] = state
    if mouse_button[GLUT_LEFT_BUTTON] == GLUT_DOWN:
        click_pos = GetOGLPos(x,y)
        nearest_point = getNearestPoint(click_pos,particle_radius)
        if nearest_point != None:
            nearest_point.pin = True
            nearest_point.col = vec3(1,0,0)
            
    elif mouse_button[GLUT_RIGHT_BUTTON] == GLUT_DOWN:
        click_pos = GetOGLPos(x,y)
        nearest_point = getNearestPoint(click_pos,particle_radius)
        if nearest_point != None:
            nearest_point.pin = False   
            nearest_point.col = vec3(1,1,1)             

def myReshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(50.0, float(w)/float(h), 0.01, 100.0)
    glMatrixMode(GL_MODELVIEW) 

def init_gl(r, g, b, a, smooth=True, depth=False):
    glClearColor(r, g, b, a)
    glShadeModel(GL_SMOOTH if smooth else GL_FLAT)
    if depth:
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
    lists = [['Vendor', GL_VENDOR], ['Renderer',GL_RENDERER],
             ['OpenGL Version', GL_VERSION], 
             ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
    
def main():
    global next_game_tick
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH) # Add Depth View to Color
    glutInitWindowSize(512,512)
    glutInitWindowPosition(100,100)
    glutCreateWindow(b"Mass-Spring Models Test 0.1")
    glutInit()
    glutDisplayFunc(myDisplay)
    glutIdleFunc(myIdle) 
    glutReshapeFunc(myReshape)  
    glutMouseFunc(myMouse)
    glutMotionFunc(myMotion)     
    glEnable(GL_DEPTH_TEST) #Use Depth Function  to enable view
    init_gl(0, 0, 0, 1, depth=True, smooth=False)
    glClear(GL_COLOR_BUFFER_BIT)  
    
    initCloth()
    
    next_game_tick = glutGet(GLUT_ELAPSED_TIME)
    
    glutMainLoop() 
   
def writeStrokeString(x, y, msg, font=GLUT_STROKE_ROMAN):
    prev_width = glGetFloatv(GL_LINE_WIDTH)
    glTranslatef(x, y, 0)
    glScalef(0.25, 0.15, 0.25)
    glLineWidth(2.0)
    glEnable(GL_LINE_SMOOTH)
    for i in msg:
        glutStrokeCharacter(font, ord(i))        
    glLineWidth(prev_width)
    glDisable(GL_LINE_SMOOTH)

def writeBitmapString(x, y, msg, font=GLUT_BITMAP_8_BY_13):
    glRasterPos2f(x, y)
    for i in msg:
        glutBitmapCharacter(font, ord(i))

def writeMessage(msg, x=20, y=20, stroke=False,
                 win_w=640, win_h=480, color=[0,1,0]):
    prev_mode = glGetIntegerv(GL_MATRIX_MODE)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, win_w, 0, win_h, -1, 1)
    glColor3fv(color)
    if stroke:
        writeStrokeString(x, y, msg)
    else:
        writeBitmapString(x, y, msg)
    glPopMatrix()
    glMatrixMode(prev_mode)  
       
if __name__ == "__main__":
    main()      
