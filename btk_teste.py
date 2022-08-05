import sys
#sys.path.append("C:\\Python38\\Lib\\site-packages\\btk")
sys.path.append("C:\Python38\Lib\site-packages\btk")
sys.path.append("C:/Python38/Lib/site-packages/btk")
import btk

class BTK:
    def __init__(self):
      print('Init')
    
    def processaArquivo(self, nomeArquivo):
      reader = btk.btkAcquisitionFileReader()

      reader.SetFilename(nomeArquivo)
      reader.Update()
      acq = reader.GetOutput()

      metadata = acq.GetMetaData()

      qtd_dados_tuple = metadata.FindChild("ANALYSIS").value().FindChild("USED").value().GetInfo().ToInt()

      nome_dado = metadata.FindChild("ANALYSIS").value().FindChild("NAMES").value().GetInfo().ToString()
      valor_dado = metadata.FindChild("ANALYSIS").value().FindChild("VALUES").value().GetInfo().ToDouble()
      lado_dado = metadata.FindChild("ANALYSIS").value().FindChild("CONTEXTS").value().GetInfo().ToString()
      unidade_dado = metadata.FindChild("ANALYSIS").value().FindChild("UNITS").value().GetInfo().ToString()

      for i in range(0, qtd_dados_tuple[0]):
        print(nome_dado[i]+ "  |  " + lado_dado[i]+ "  |  " + str(valor_dado[i]) + "  |  " + unidade_dado[i])

btk1 = BTK()
btk1.processaArquivo("A13F22RJ03")