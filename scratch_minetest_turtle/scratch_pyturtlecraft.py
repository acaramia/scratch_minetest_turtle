#! /usr/bin/python

# Scratch Helper app
# ------------------
# template based on work of Chris Proctor, Project homepage: http://mrproctor.net/scratch
#   https://github.com/cproctor/scratch_hue
#
# main document
#   https://wiki.scratch.mit.edu/w/images/ExtensionsDoc.HTTP-9-11.pdf
# Scratch Extension Protocol Discussion
#   https://wiki.scratch.mit.edu/wiki/Scratch_Extension
#   https://scratch.mit.edu/discuss/topic/18117/
# scratchx extension
#   https://github.com/LLK/scratchx/wiki
# hat blocks
#   https://scratch.mit.edu/discuss/topic/49736/
# wedo extension
#   https://scratch.mit.edu/scratchr2/static/js/scratch_extensions/wedoExtension.js
# framework scratch/snap
#   https://github.com/blockext/blockext/tree/master/blockext
# flask objects
#   http://flask.pocoo.org/docs/0.12/api/
#

# install Flask (conda install flask)
# pip install pycraft-minetest

#
# TODO blocco over non funziona, provare con true invece di True
# TODO blocco per leggere la chat e inserire le risposte in say
# TODO blocco hat vedere cone funziona
#
# TODO [" ", "point in direction %n", "pointto", 90],
# TODO [" ", "set pen to block type %m.blocktype", "penblock", "ice"],
# TODO mettere i colori delsetblock come menu wool e poi un setblock libero con nome materiale
#

from flask import Flask, request
import logging
import pycraft_minetest as pcmt
import time
from PycraftMaterialsLibrary import PycraftMaterialsLibrary

""" 
  global variables
"""
app = Flask("Scratch_Pycraft")
EXTENSION_PORT = 3320
myturtle = None
jobs = set()  # jobs keeps the waiting jobs id. blocks type:'w'
variables = {}  # addVariable to return values to scratch (blocks type: 'r')
materialLibray = PycraftMaterialsLibrary()

def initLogger(app):
    """ initialize logger, app to DEBUG and flask to ERROR """
    from sys import stdout
    app.logger.removeHandler(app.logger.handlers[0])
    loggers = [[app.logger, logging.DEBUG, logging.StreamHandler(stdout)],
               [logging.getLogger('werkzeug'), logging.ERROR, logging.NullHandler()]]
    # handler = logging.FileHandler('"Scratch_Pycraft".log')
    formatter = logging.Formatter('%(asctime)s - %(name)14s - %(levelname)s - %(message)s')
    for logger in loggers:
        handler = logger[2]
        handler.setFormatter(formatter)
        logger[0].addHandler(handler)
        logger[0].setLevel(logger[1])


@app.errorhandler(Exception)
def exceptions(e):
    app.logger.debug(e)

@app.before_request
def after_request():
    if request.path != "/poll": # to avoid not necessary logs
        app.logger.debug("received {}".format(request.full_path))

# scratch protocol path
@app.route('/poll')
def poll():
    global myturtle, jobs, variables
    where() # update position
    s = "\n".join(["_busy {}".format(job) for job in jobs])
    s = s + "\n".join(["{} {}".format(var, variables[var]) for var in variables.keys()])
    #b = s
    #if b.strip() != "":
    #    print(b)
    return s

@app.route('/reset_all')
def reset_all():
    global myturtle, jobs, variables
    jobs = set()
    variables = {}
    return "OK"

@app.route('/crossdomain.xml')
def cross_domain_check():
    return '<cross-domain-policy><allow-access-from domain="*" to-ports="'+EXTENSION_PORT+'"/></cross-domain-policy>'

# PYCRAFT FUNCTIONS:

def log(s):
    app.logger.debug("executing {}".format(s))
    pcmt.chat("turtle received: {}".format(s))

def addVariable(varName, varValue):
    global myturtle, jobs, variables
    variables[varName] = str(varValue)

@app.route('/reset_turtle')
def reset_turtle():
    global myturtle, jobs, variables
    myturtle = initTurtle()
    return "OK"

def where():
    """
       called from poll to update position and block under feet
       warning: poll calls us 30 times for second
       if it slow down everything, we should cache the position and update 1 or 2 times every second
    """
    global myturtle, jobs, variables
    pos = pcmt.where()
    und = pcmt.under() #pcmt.what(0, -1, 0, absolute=False)
    undName = materialLibray.getBlockName(und)
    addVariable("posx", pos.x)
    addVariable("posy", pos.y)
    addVariable("posz", pos.z)
    addVariable("what", undName)
    return "OK"

@app.route('/penup/<int:jobId>')
def penup(jobId):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("penup")
    myturtle.penup()
    jobs.remove(jobId)
    return "OK"

@app.route('/pendown/<int:jobId>')
def pendown(jobId):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("pendown")
    myturtle.pendown()
    jobs.remove(jobId)
    return "OK"

@app.route('/up/<int:jobId>/<int:angle>')
def up(jobId,angle):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("up {}".format(angle))
    myturtle.up(angle)
    jobs.remove(jobId)
    return "OK"

@app.route('/down/<int:jobId>/<int:angle>')
def down(jobId, angle):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("down {}".format(angle))
    myturtle.down(angle)
    jobs.remove(jobId)
    return "OK"

@app.route('/forward/<int:jobId>/<int:steps>')
def forward(jobId, steps):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("forward {}".format(steps))
    myturtle.forward(steps)
    jobs.remove(jobId)
    return "OK"

@app.route('/left/<int:jobId>/<int:degrees>')
def left(jobId, degrees):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("left {}".format(degrees))
    myturtle.left(degrees)
    jobs.remove(jobId)
    return "OK"

@app.route('/right/<int:jobId>/<int:degrees>')
def right(jobId, degrees):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("right {}".format(degrees))
    myturtle.right(degrees)
    jobs.remove(jobId)
    return "OK"

@app.route('/goto/<int:jobId>/<int:x>/<int:y>/<int:z>')
def goto(jobId, x, y, z):
    global myturtle, jobs, variables
    jobs.add(jobId)
    log("goto x {} y {} z {}".format(x, y, z))
    myturtle.goto(x, y, z)
    jobs.remove(jobId)
    return "OK"

@app.route('/penblock/<int:jobId>/<string:block>')
def penblock(jobId, block):
    global myturtle, jobs, variables
    jobs.add(jobId)
    id = materialLibray.getBlockId(block)
    log("penblock {}[{}]".format(block, id))
    myturtle.penblock(id)
    jobs.remove(jobId)
    return "OK"

"""
@app.route('/cube/<int:jobId>/<string:block>/<int:side>/<int:x>/<int:y>/<int:z>')
def cube(jobId, block, side, x, y, z):
    global myturtle, jobs, variables
    jobs.add(jobId)
    print(block, side, x, y, z)
    pcmt.cube(pcmt.getblock(block), side, x, y, z)
    jobs.remove(jobId)
    return "OK"
"""

def initTurtle():
    t = pcmt.Turtle(pcmt.glowstone)
    t.clear_turtle(0, 0, 0)
    t.setheading(0)
    t.setverticalheading(0)
    t.setposition(0, 0, 0)
    t.speed(12) # create a block for speed?
    pcmt.chat("turtle created")
    app.logger.debug("turtle created {}".format(str(t)))
    return t

def main():
    global app, myturtle, EXTENSION_PORT
    initLogger(app)
    print(" **************************************************")
    print(" * The Scratch helper app is running. Have fun :) *")
    print(" *                                                *")
    print(" *** creating turtle ***                          *")
    print(" * Press Control + C to quit.                     *")
    print(" **************************************************")

    myturtle = initTurtle()

    done = False
    while not done:
        try:
            app.run('0.0.0.0', port=EXTENSION_PORT)
        except:
            print("trying again")
            time.sleep(1)
        else:
            print("scratch_pyturtlecraft done")
            done = True


if __name__ == "__main__":
    main()
