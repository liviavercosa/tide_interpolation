import csv 
from datetime import datetime

##################################################################
#	ATENÇÃO:
#	Incluir o ponto de inflexão anterior ao início do intervalo
#	Incluir o próximo ponto de inflexão após o fim do intervalo
##################################################################

# Arquivo deve esta na pasta in_data com o nome neste padrão:
# "in_data/mares_[MES]_[ANO]_[LOCAL].txt"
ano = "2006" 
mes = "julho"
local = "porto_recife"
file = open("in_data/mares_"+mes+"_"+ano+"_"+local+".txt","r") 
with open("out_data/mares_"+mes+"_"+ano+"_" +local+".csv", 'w', newline='') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	spamwriter.writerow(['DATAHORA','ALTURA'])
	for line in file: 
		line  = line.replace("\n", "")
		if len(line) == 5 :
			data = line + "/" + ano
		else:
			altura = line[-3:]
			hora = line[:5]
			dataHora = datetime.strptime(data + " " + hora, "%d/%m/%Y %H:%M")
			spamwriter.writerow([dataHora,altura])