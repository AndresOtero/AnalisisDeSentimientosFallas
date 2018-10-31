import csv
def parse(filename):
	csvfile= open(filename, 'r') 
	reader=csv.reader(csvfile,delimiter=',')
	rowNames=next(reader)
	print(rowNames)
	rowNames[0]="ID"
	diccRowNames={}
	i=0
	for rowName in rowNames:
		print( rowName)
		diccRowNames[rowName]=i
		i=i+1
	print (diccRowNames)
	rows=[]
	for row in reader:
		rows.append(row)
	return rowNames,diccRowNames,rows

def filtrarSinCategorias(rows,diccRowNames,categorias):
	print (categorias)
	indices= ([ diccRowNames[categoria] for categoria in categorias])
	print (indices)
	for categoria in categorias:
		newRows=[]
		for row in rows:
			if(row[diccRowNames[categoria]]):
				newRows.append(row)
		rows=newRows
	newRows=[]
	for row in rows:
		newRow =[ row[indice] for indice in indices]
		newRows.append(newRow)
	rows=newRows
	return newRows

def contarCategorias(rows,diccRowNames,categoria):
	diccFreq={}
	for row in rows:
		element=row[diccRowNames[categoria]]
		if(element in diccFreq):
			diccFreq[element]+=1
		else:
			diccFreq[element]=1
	return diccFreq

def cambiarCategorias(rows,diccRowNames,categoria,valores,nuevaCategoria):
	for row in range(len(rows)):
		for valor in valores:
			if(rows[row][diccRowNames[categoria]]==valor):
				rows[row][diccRowNames[categoria]]=nuevaCategoria
	return rows

def categoriasAEleminar(diccFreq,minimo):
	return [cat for cat in diccFreq if diccFreq[cat]<minimo]

def calcularSentimientoComentario(rows,diccRowNames):
	newRows=[]
	for row in rows:
		newRow=[]
		Rating=int(row[diccRowNames["Rating"]])
		Recommended=int(row[diccRowNames["Recommended IND"]])
		PositiveFeedbackCount=row[diccRowNames["Positive Feedback Count"]]
		if(Rating==3 or (Rating==4 and Recommended==0) or (Rating==2 and Recommended==1) ):
			newRow=[row[diccRowNames["Review Text"]]]+["NEUTRA"]
		elif(Rating>=4):
			newRow=[row[diccRowNames["Review Text"]]]+["POSITIVA"]
		elif(Rating<=2):
			newRow=[row[diccRowNames["Review Text"]]]+["NEGATIVA"]
		newRows.append(newRow)
	diccRowNames={}
	diccRowNames["Review Text"]=0
	diccRowNames["Sentimiento"]=1

	return diccRowNames,newRows

def replaceCategoriaPorNumero(rows,cat_number):
	newRows=[]
	dicc={}
	i=0
	for row in rows:
		cat= row[cat_number]
		newRow=[x for x in row]
		if cat not in dicc:
			dicc[cat]=i
			i+=1
		newRow[cat_number]=dicc[cat]
		newRows.append(newRow)
	return dicc,newRows

rowNames,diccRowNames,rows=parse('reviews.csv')
categoriasAFiltrarSentimientos=["Recommended IND","Rating","Positive Feedback Count","Review Text"]
diccSentimientos={}
i=0
for cat in categoriasAFiltrarSentimientos:
	diccSentimientos[cat]=i
	i+=1

categoriasAFiltrarClassName=["Review Text","Class Name"]

diccClassName={}
i=0
for cat in categoriasAFiltrarClassName:
	
	diccClassName[cat]=i
	i+=1

newRows=[]
for row in rows:
	newRow= []
	for r in row:
		newRow.append(	r.replace("\n", " "))
	newRows.append(newRow)
print(diccClassName)

rows=newRows
rowsSentimientos=filtrarSinCategorias(rows,diccRowNames,categoriasAFiltrarSentimientos)
print ("Sentimientos: "+ str(len(rowsSentimientos)))
rowsClassName=filtrarSinCategorias(rows,diccRowNames,categoriasAFiltrarClassName)
print ("ClassName: "+ str(len(rowsClassName)))
diccFreq=contarCategorias(rowsClassName,diccClassName,"Class Name")
print(diccFreq)





diccSentimientos,rowsSentimientos=calcularSentimientoComentario(rowsSentimientos,diccSentimientos)
print ("Sentimientos: "+ str(len(rowsSentimientos)))
diccFreq=contarCategorias(rowsSentimientos,diccSentimientos,"Sentimiento")
print(diccFreq)

print(rowsClassName[1])
diccCategoryClassName,rowsClassName_Numbers=replaceCategoriaPorNumero(rowsClassName,1)
print(rowsClassName[1])
print(diccCategoryClassName)
diccCategorySentiment,rowsSentimientos_Numbers=replaceCategoriaPorNumero(rowsSentimientos,1)
print(diccCategorySentiment)

with open('reviewsSentimientos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Review Text","Sentimiento"])
    for row in rowsSentimientos:
    	writer.writerow(row)

with open('reviewsClassName.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(categoriasAFiltrarClassName)
    for row in rowsClassName:
    	writer.writerow(row)
