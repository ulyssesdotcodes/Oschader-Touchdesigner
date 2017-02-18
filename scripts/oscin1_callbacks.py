# me - this DAT
# 
# dat - the DAT that received a message
# rowIndex - the row number the message was placed into
# message - an ascii representation of the data
#           Unprintable characters and unicode characters will
#           not be preserved. Use the 'bytes' parameter to get
#           the raw bytes that were sent.
# bytes - a byte array of the message.
# timeStamp - the arrival time component the OSC message
# address - the address component of the OSC message
# args - a list of values contained within the OSC message
# peer - a Peer object describing the originating message
#   peer.close()    #close the connection
#   peer.owner  #the operator to whom the peer belongs
#   peer.address    #network address associated with the peer
#   peer.port       #network port associated with the peer
#

toEffectsDict = {}
fromEffectsDict = {}

toInputsDict = {}

def receiveOSC(dat, rowIndex, message, bytes, timeStamp, address, args, peer):
  if(len(args) > 0):
    global toEffectsDict
    global fromEffectsDict
    global toInputsDict

    opName = args[0]
    uniforms = op('uniforms_' + opName)
    curOp = op(opName)

    if(address != "/progs/uniform"):
      print(message)

    if(address == "/progs"):
      progType = args[1]

      if(curOp != None and curOp.par.Program != progType):
        curOp.destroy()
        curOp = None
        uniforms.destroy()
        uniforms = None

      if(uniforms == None):
        uniforms = parent().create(tableDAT, 'uniforms_'+opName)
        uniforms.export = True
        # uniforms.expose = False
        uniforms.appendRow(["", "path", "parameter", "value"])
        uniforms.deleteRow(0)

      newProg = op(progType)
      if(newProg != None and curOp == None):
        curOp = op('/project1').copy(op(newProg))
        curOp.name = opName

      if (opName in fromEffectsDict):
        fromOp = op(fromEffectsDict[opName])
        if(fromOp != None):
          if(len(fromOp.outputConnectors[0].connections) > 0):
            curOp.outputConnectors[0].connect(fromOp.outputs[0].inputConnectors[0])
          fromOp.outputConnectors[0].connect(curOp.inputConnectors[0])

      if(opName in toEffectsDict):
        toOp = op(toEffectsDict[opName])
        if(toOp != None):
          curOp.outputConnectors[0].connect(toOp.inputConnectors[0])

      baseName = prog_name(opName)

      if len(curOp.pars('Base')) > 0:
        curOp.par.Base = "../" + baseName + "_base"

      if opName[len(baseName):] == '0':
        baseOp = op(baseName + "_base")

        if baseOp == None:
          baseOp = op('/project1').create(nullTOP)
          baseOp.name = baseName + "_base"

        related = curOp.ops(baseName + '[1-99]')

        if len(related) == 0:
          curOp.outputConnectors[0].connect(baseOp)
        else:
          curOp.outputConnectors[0].connect(related[0])
          related[-1].connect(baseOp)

        if(opName == "s0"):
          baseOp.outputConnectors[0].connect(op('sout'))

        if(opName == "t0"):
          baseOp.outputConnectors[0].connect(op('tout'))

      toInputsDict[opName] = []


    elif (address == "/progs/effect"):
      toEffectsDict[opName] = args[1]
      fromEffectsDict[args[1]] = opName
      effOp = op(args[1])
      if(effOp != None):
        print(curOp.name + " -> " + effOp.name)
        if(len(curOp.outputs) > 0):
          nextOp = curOp.outputs[0]
          effOp.outputConnectors[0].connect(nextOp.inputConnectors[0])
        curOp.outputConnectors[0].connect(effOp.inputConnectors[0])

    elif (address == "/progs/effect/clear"):
      if (opName in toEffectsDict):
        delete_effect(toEffectsDict[opName])


    elif (address == "/progs/uniform" and uniforms != None):
      uName = args[1]
      val = 0
      if args[2] == "input":
        inputs = toInputsDict[opName]
        newOpName = opName + '_input_' + uName

        newOp = op(newOpName)

        if newOp != None:
          if newOp.par.Type != args[3]:
            op(newOpName).destroy()
            newOp = op('/project1').copy(op(args[3]))
            inputs.append(newOp.name)
        else:
            newOp = op('/project1').copy(op(args[3]))
            inputs.append(newOp.name)

        newOp.name = newOpName
        toInputsDict[opName] = inputs
        val = "op('" + newOp.name + "').op('out1')"
        if type(newOp.op('out1')) == outCHOP:
          val += "[0]"
        if len(args) > 4:
          newOp.par.In1 = args[4]
        if len(args) > 5:
          newOp.par.In2 = args[5]
        if len(args) > 6:
          newOp.par.In3 = args[6]
      elif args[2] == "string":
        val = "\"" + args[3].strip() + "\""
      else:
        val = args[2]

      uni = uniforms.row(uName)
      if(uni != None and len(uni) > 0):
        uni[3].val = val
      else:
        uniforms.appendRow([uName, opName, uName.replace("_", "").capitalize(), val])

    elif (address == "/progs/clear" and uniforms != None):
      delete_effect(opName)

  return

def delete_effect(opName):
  print("deleting " + opName)
  if (opName in toEffectsDict):
    effName = toEffectsDict[opName]
    delete_effect(effName)
    del toEffectsDict[opName]

  curOp = op(opName)
  if(curOp != None):
    curOp.inputs[0].outputConnectors[0].connect(curOp.outputs[0].inputConnectors[0])
    curOp.destroy()

  if(op('uniforms_' + opName) != None):
    op('uniforms_' + opName).destroy()

def clear_dicts():
  toEffectsDict = {}
  fromEffectsDict = {}
  toInputsDict = {}

def prog_name(prog):
  return prog.translate({ord(k): None for k in '0123456789'})
