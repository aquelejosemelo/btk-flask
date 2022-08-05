import c3d
from c3d.scripts.c3d_metadata import print_metadata
from itertools import product

class Analysis:
  def __init__(self, context, description, name, subject, unit, value):
    self.context = context
    self.description = description
    self.name = name
    self.subject = subject
    self.unit = unit
    self.value = value

class BTK:
  def __init__(self, nomeArquivo):
    self.nomeArquivo = nomeArquivo
  
  def processaArquivo(self):
    with open(self.nomeArquivo, 'rb') as handle:
      reader = c3d.Reader(handle)
      for i, (points, analog) in enumerate(reader.read_frames()):
          print('Frame {}: {}'.format(i, points.round(2)))
  
  def printMetadata(self):
    with open(self.nomeArquivo, 'rb') as handle:
      reader = c3d.Reader(handle)
      print_metadata(reader)
  
  def listar_analysis_metadata(self):
    with open(self.nomeArquivo, 'rb') as handle:
      reader = c3d.Reader(handle)

      lValues = []
      lDescriptions = []
      lUnits = []
      lNames = []
      lContexts = []
      lSubjects = []
      used = 0
      for key, g in sorted(reader.group_items()):
        if (g.name == 'ANALYSIS'):
          for key, p in sorted(g.param_items()):
            pTmp = self.get_param(g, p)
            if (p.name == 'VALUES'):
              lValues = pTmp
            elif (p.name == 'DESCRIPTIONS'):
              lDescriptions = pTmp
            elif (p.name == 'UNITS'):
              lUnits = pTmp
            elif (p.name == 'NAMES'):
              lNames = pTmp
            elif (p.name == 'CONTEXTS'):
              lContexts = pTmp
            elif (p.name == 'SUBJECTS'):
              lSubjects = pTmp
            elif (p.name == 'USED'):
              used = pTmp

      lAnalysis = []
      for i in range(used):
        analysisTmp = Analysis(
          lContexts[i],
          lDescriptions[i],
          lNames[i],
          lSubjects[i],
          lUnits[i],
          lValues[i]
        )

        lAnalysis.append(analysisTmp)
      return lAnalysis

  def get_param_value(self, value):
    return value

  def get_param_array(self, p, offset_in_elements):
    arr = []
    start = offset_in_elements
    end = offset_in_elements + p.dimensions[0]
    if p.bytes_per_element == 2:
        arr = p.int16_array
    elif p.bytes_per_element == 4:
        arr = p.float_array
    elif p.bytes_per_element == -1:
        return self.get_param_value(p.bytes[start:end])
    else:
        arr = p.int8_array
    return arr.flatten()[start:end]

  def get_param(self, g, p):
    if len(p.dimensions) == 0:
      val = None
      width = len(p.bytes)
      if width == 2:
          val = p.int16_value
      elif width == 4:
          val = p.float_value
      else:
          val = p.int8_value
      return self.get_param_value(val)

    if len(p.dimensions) == 1 and p.dimensions[0] > 0:
      return self.get_param_array(p, 0)

    if len(p.dimensions) >= 2:
      offset = 0
      listaTmp = []
      for coordinate in product(*map(range, reversed(p.dimensions[1:]))):
        subscript = ''.join(["[{0}]".format(x) for x in coordinate])
        listaTmp.append(self.get_param_array(p, offset))
        offset += p.dimensions[0]
      return listaTmp

btk1 = BTK("A13F22RJ03.c3d")
# btk1.processaArquivo("A13F22RJ03.c3d")
#btk1.printMetadata("A13F22RJ03.c3d")
lAnalysis = btk1.listar_analysis_metadata()
