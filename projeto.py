from pymaps import Map,PyMap,Icon
from tabulate import tabulate as tb
import csv
import sys
import os
import webbrowser
import numpy as np

def show_table(table):
        """Prints a table with tabulate 0.7.2.
For more information of this module visit: https://pypi.python.org/pypi/tabulate/0.7.2.
"""

        print(tb(table[1:],table[0],"grid"))  
        return 'Thanks tabulate'
        
def file_to_table():
        """Returns the table read from the file."""
        table=[]
        with open('FactSelec.csv', 'r') as file:
                reader=csv.reader(file)
                for row in reader:
                        table.append(row)
                file.close()
        return table

def add_criteria(temptable):
        """Returns a new table with a new line"""
        criterialst=[]

        for j in range (len(temptable[0])):
                print('\n---> ',temptable[0][j])
                value=str(eval(input('Introduza o valor:')))
                
                if j==0:
                        while value.isdigit():#validar strings
                                print('Deve introduzir um fator valido.')
                                value=str(eval(input('Introduza o valor:')))
                else:
                        while not value.replace(".", "", 1).isdigit():#este replace() permite validar inteiros e floats
                                print('Deve introduzir um valor numerico')
                                value=str(eval(input('Introduza o valor:')))
                                
                criterialst.append(value)
        temptable.append(criterialst)
        return temptable
            
def delete_criteria(temptable):
        """Returns a table without the choosen line of a criteria."""
        flag=False #esta variavel permite verificar se o criterio existe no array
    
        criteria=str(eval(input('Fator a eliminar:')))#este str() permite verificar tb os numeros para comparacao
        
        for i in range(temptable[:,0].size):
                if temptable[i][0].lower()==criteria.lower():#a funcao nao e senvivel a maiusculas e minusculas
                        temptable=np.delete(temptable,i,0)
                        flag=True
                        break
        return temptable,flag

def validation():
        """Validates saves and exit."""
        v_input=input('\nDeseja continuar?(S/N):')
        if v_input.upper() in ['S','SIM']:
                return True

def save_file(file_name,table):
        """Saves list of list to a file with csv module."""
        with open (file_name,'w') as file:
                wr = csv.writer(file)
                wr.writerows(table)  
                file.close()

    
def method_wsc(table):
        """Method WSC."""
        rtable=np.copy(table)
        rtable=np.delete(table,1,1)#tabela dos scores relativos
        solution=np.zeros((np.size(table[:,0])-1,np.size(table[0,:])-2),dtype=float)#esta variavel facilita o calculo da soma, media e desvio padrao
        gtable=[['City','Average','Deviation','Final score']]#tabela dos scores globais
        bscore=0

        for i in range(1,table[:,0].size):
                for j in range(2,table[0,:].size):
                        solution[i-1][j-2]=float(table[i][1])*int(table[i][j])
                        rtable[i][j-1]=float(table[i][1])*int(table[i][j])
        
        for j in range(solution[0,:].size):
                gtable.append([table[0][j+2],np.average(solution[:,j]),np.std(solution[:,j]),float(sum(solution[:,j]))])
                if bscore<float(sum(solution[:,j])):
                        bscore=float(sum(solution[:,j]))
                        bcity=table[0][j+2]                
        
        for i in range(1,len(gtable)):
                if gtable[i][0]==bcity:
                        gbest=[gtable[0],gtable[i]]         
        
        return rtable.tolist(),gtable,bcity,gbest

def show_map(bcity):
        """Shows a map in your default browser with sites marked"""
        print('\n---> Gerar Visualizacao Grafica dos Scores obtidos por Site de Localizacao\n')
        zoom=int(eval(input('Zoom(4):')))
        
        tmap = PyMap()
        tmap.maps[0].center = (46.0000,7.0000)    
        tmap.key='AIzaSyCj-UAqhnY-fhkeCEayjALakrGJMgcaQ6A'
        tmap.maps[0].zoom = zoom
        blue_icon = Icon('blue_icon')               
        blue_icon.image = "http://www.clker.com/cliparts/B/B/1/E/y/r/marker-pin-google-md.png" 
        blue_icon.iconSize = (15,25)
        tmap.addicon(blue_icon)          
        red_icon = Icon('red_icon')             
        red_icon.image = "http://www.clker.com/cliparts/e/3/F/I/0/A/google-maps-marker-for-residencelamontagne-md.png" 
        red_icon.iconSize = (15,25)
        tmap.addicon(red_icon)    
        
        file=open('coords.csv','r')
        reader=csv.reader(file)
        
        for row in reader:           
                if row[0]==bcity:
                        p=[row[1],row[2],row[0][3:],'blue_icon']
                        tmap.maps[0].setpoint(p)

                else:
                        p=[row[1],row[2],row[0][3:],'red_icon']
                        tmap.maps[0].setpoint(p)   

        file.close()             
        open('mymap.html','w').write(tmap.showhtml())
        filepath = os.path.abspath('mymap.html') 
        webbrowser.open('file://' + filepath)   
        
        return '\nMapa guardado!'
        
if __name__=='__main__':
        while True:
                print('\nMENU\n----\n1-Ler informacao sobre os pontos da rede\n2-Determinacao do Score de Localizacao para efeitos de Decisao\n3-Gerar Visualizacao Grafica dos Scores obtidos por Site de Localizacao\n4-Salvaguardar informacao do Site Selecionado pelo metodo WSC\n5-Eliminar um factor de selecao da localizacao da rede logistica\n6-Criar novo factor de selecao da localizacao da rede logistica\n0-Sair do programa')
                try:
                        option=eval(input('\nInsira a opcao que pretende:'))
                
                        if option in [0,'0']:
                                print('\n---> SAIR')
                                if validation():
                                        break
                        
                        elif option in [1,'1']:
                                table=file_to_table()
                                print('\n---> Ler informacao sobre os pontos da rede')
                                print('\n>> Informacao sobre os pontos da rede')
                                show_table(table)
                                
                        
                        elif option in [2,'2']:
                                rtable,gtable,bcity,gbest=method_wsc(np.array(table))
                                print('\n---> Determinacao do Score de Localizacao para efeitos de Decisao')
                                print('\n>> Scores relativos')
                                show_table(rtable)                                
                                print('\n>> Scores globais')
                                show_table(gtable)
                                print('\n>> Site selecionado:',bcity[3:])
                                                              
                                flag2=True# esta variavel permite verificar se a opcao 2 foi executada 

                        elif option in [3,'3']:
                                
                                show_map(bcity)
                        
                        elif option in [4,'4']:
                                if flag2:
                                        print('\n---> Salvaguardar informacao do Site Selecionado pelo metodo WSC')
                                        print('\n>> Scores globais do site selecionado')                                
                                        show_table(gbest)
                                        if validation():
                                                save_file('SiteSelec.csv',gbest)
                                                print('\nFicheiro guardado com sucesso.')
         
                        elif option in [5,'5']:
                                print('\n---> Eliminar um factor de selecao da localizacao da rede logistica')
                                print('\n>> Informacao sobre os pontos da rede')
                                show_table(table)
                                temptable,flag=delete_criteria(np.array(table))
                                if flag:
                                        print('\n>> Informacao sobre os pontos da rede actualizado')
                                        show_table(temptable.tolist())
                                        if validation():
                                                save_file('FactSelec.csv',temptable.tolist())
                                                print('\nFator removido com sucesso') 
                                                del table,temptable,flag
                                                if 'flag2' in globals():# verifica se a variavel existe
                                                        del rtable,gtable,bcity,gbest,flag2
                                                        
                                else:
                                        print('\nERRO!Introduza um fator valido.')   

                        elif option in [6,'6']: 

                                        show_table(table)
                                        temptable=add_criteria(table)
                                        show_table(temptable)
                                          
                                        if validation():
                                                save_file('FactSelec.csv',temptable)
                                                print('Novo fator adicionado com sucesso')
                                                del table,temptable,flag
                                                if 'flag2' in globals():
                                                        del rtable,gtable,bcity,gbest,flag2                                                
                        else:
                                print('\nERRO!Introduza uma opcao valida.')
                except FileNotFoundError:
                        print('\nERRO!Ficheiro nao encontrado.')
                except IndexError:
                        print('\nERRO!Verifique o conteudo do ficheiro.')
                except NameError:
                        print('\nERRO!\n1.Para a opcao 2,5 e 6 deve executar primeiro a opcao 1.\n2.Para opcao 3 e 4 deve executar primeiro a opcao 2.\n3.Caso queira introduzir uma string deve colocar entre plicas.')     
                except SyntaxError:
                        print('\nERRO!Caso queira introduzir uma string deve colocar entre plicas.')
                        
