import csv

def parse(filename):
	csvfile= open(filename, 'r') 
	reader=csv.reader(csvfile,delimiter=',')
	rowNames=next(reader)
	rowNames[0]="ID"
	diccRowNames={}
	i=0
	for rowName in rowNames:
		diccRowNames[rowName]=i
		i=i+1
	rows=[]
	for row in reader:
		rows.append(row)
	return rowNames,diccRowNames,rows

def filtrarSinCategorias(rows,diccRowNames,categorias):
	indices= ([ diccRowNames[categoria] for categoria in categorias])
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
		PositiveFeedbackCount=int(row[diccRowNames["Positive Feedback Count"]])
		#if ((Rating==5 and Recommended==0) or(Rating<=2 and Recommended==1)):#or (PositiveFeedbackCount==0)):
		#	continue
		if(Rating==3):
			newRow=["'"+row[diccRowNames["Review Text"]]+"'"]+["NEUTRA"]
		elif(Rating>=4):
			newRow=["'"+row[diccRowNames["Review Text"]]+"'"]+["POSITIVA"]
		elif(Rating<=2):
			newRow=["'"+row[diccRowNames["Review Text"]]+"'"]+["NEGATIVA"]
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

def makeDiccCategoriesToFilter(categoriasAFiltrar): 
	diccClassName={}
	i=0
	for cat in categoriasAFiltrar:
		diccClassName[cat]=i
		i+=1
	return diccClassName

def filterBadCharactersfromRows(rows):
	newRows=[]
	for row in rows:
		newRow= []
		for r in row:
			r1=r.replace("\n", ".")
			r2=r1.replace('"',".")
			r3=r2.replace('/',".")
			r4=r3.replace(',',".")
			r5=r4.replace("'",".")
			r6=r5.replace('-',".")
			newRow.append(r6)
		newRows.append(newRow)
	return newRows


def filterCategories(rows,cat,categories):
	newRows=[]
	for row in rows:
		if row[cat] not in categories:
			newRows.append(row)
	return newRows



rowNames,diccRowNames,rows=parse('reviews.csv')
categoriasAFiltrarSentimientos=["Recommended IND","Rating","Positive Feedback Count","Review Text"]
diccSentimientos=makeDiccCategoriesToFilter(categoriasAFiltrarSentimientos)
categoriasAFiltrarClassName=["Review Text","Class Name"]
diccClassName=makeDiccCategoriesToFilter(categoriasAFiltrarClassName)

rows=filterBadCharactersfromRows(rows)
rowsSentimientos=filtrarSinCategorias(rows,diccRowNames,categoriasAFiltrarSentimientos)
rowsClassName=filtrarSinCategorias(rows,diccRowNames,categoriasAFiltrarClassName)
diccFreq=contarCategorias(rowsClassName,diccClassName,"Class Name")
print(diccFreq)
categoriesToFilter=[x for x in diccFreq if diccFreq[x]<10]
rowsClassName=filterCategories(rowsClassName,1,categoriesToFilter)
diccFreq=contarCategorias(rowsClassName,diccClassName,"Class Name")
print(diccFreq)
diccSentimientos,rowsSentimientos=calcularSentimientoComentario(rowsSentimientos,diccSentimientos)
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
print("Se han generado reviewsSentimientos.csv y reviewsClassName.csv")