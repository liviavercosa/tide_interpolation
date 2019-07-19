import csv 
import pandas as pd 
from datetime import datetime
from pandas import Series, DataFrame  
import matplotlib.pyplot as plt  
import matplotlib as mpl 

#######################################################
#	
#
#
#######################################################
mes = 'julho'
ano = '2006'
local = "porto_recife"
start = datetime.strptime("01/07/2006", "%d/%m/%Y")
end = datetime.strptime("01/08/2006", "%d/%m/%Y")

index = pd.date_range(start, end)
df = pd.DataFrame(index=index, columns=['ALTURA', 'INFLEXAO', 't', 'T', 'n1', 'n2', 'h1', 'h2'])
df = df.asfreq('10Min')
df['INFLEXAO'] = False
df.index.name = "DATAHORA"

csv.register_dialect('MyDialect', delimiter='\t', quotechar='"', skipinitialspace=True, quoting=csv.QUOTE_NONE, lineterminator='\n', strict=True)


with open('out_data/mares_'+mes+'_'+ano+'_'+local+'.csv','r') as csvfile:
    reader = csv.DictReader(csvfile, dialect='MyDialect')
    delta_time_min = 0
    for row in reader:
    	df.at[datetime.strptime(row['DATAHORA'], "%Y-%m-%d %H:%M:%S"),'ALTURA'] = float(row['ALTURA'])
    	df.at[datetime.strptime(row['DATAHORA'], "%Y-%m-%d %H:%M:%S"),'INFLEXAO'] = True
    	df.at[datetime.strptime(row['DATAHORA'], "%Y-%m-%d %H:%M:%S"),'t'] = 0
    	df.at[datetime.strptime(row['DATAHORA'], "%Y-%m-%d %H:%M:%S"),'T'] = 0
    	
df = df.sort_index()
print(df)

dataHoraAnterior=n1=n2=''

for index, row in df.iterrows():
	if row['INFLEXAO'] == True:
		n1 = row['ALTURA']
		dataHoraAnterior = index
	else:
		row['n1'] = n1
		row['t'] = (index - dataHoraAnterior).seconds // 60 # lembrar de incluit o ultimo ponto de inflexão do mês anterior
		row['T'] = dataHoraAnterior

# df.to_csv("teste.csv",sep=',', decimal='.')
# raise Exception()
for index, row in  list(df.iterrows())[::-1]:
	if row['INFLEXAO'] == True:
		n2 = row['ALTURA']
		dataHoraAnterior = index
	else:
		row['n2'] = n2
		row['T'] = (dataHoraAnterior - row['T']).seconds // 60


for index, row in df.iterrows():
	if row['INFLEXAO'] == False:
		row['h1'] = 1 - 3*(row['t']/row['T'])**2 + 2*(row['t']/row['T'])**3
		row['h2'] = 3*(row['t']/row['T'])**2 - 2*(row['t']/row['T'])**3
		row['ALTURA'] = float(float(row['h1'])*float(row['n1']) + float(row['h2'])*float(row['n2']))

df = df.round(4)
print(df)

df.to_csv("out_data/mares_"+mes+"_"+ano+'_'+local+"_interpolado.csv",sep=',', decimal='.')

plt.plot(df.index, df.ALTURA)
plt.savefig("out_data/plot_mares_"+mes+"_"+ano+'_'+local+".png")  
plt.show()

# with open("mares_"+mes+"_"+ano+"porto_recife.csv", 'w', newline='') as csvfile:
# 	spamwriter = csv.writer(csvfile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# 	spamwriter.writerow(['DATAHORA','ALTURA'])
# 	for line in file: 
# 		line  = line.replace("\n", "")
# 		if len(line) == 5 :
# 			data = line + "/" + ano
# 		else:
# 			altura = line[-3:]
# 			hora = line[:5]
# 			dataHora = datetime.strptime(data + " " + hora, "%d/%m/%Y %H:%M")
# 			spamwriter.writerow([dataHora,altura])