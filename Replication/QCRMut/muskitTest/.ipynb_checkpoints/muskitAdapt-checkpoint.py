import os

def adapt (folderPath: str, adaptPath:str, PGZPath:str):
    
    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath,f))]

    for x in files:
        
        f = open(folderPath+"/"+x,"r")
        g = open(adaptPath+x,"w")

        g.write("import pickle\nimport gzip\n")
        g.write(f.read())
        g.write(f"\n\nwith gzip.open('{PGZPath}{x[:-3]}.pgz',mode='wb') as f:\n    pickle.dump(qc,f)\nf.close()")
        g.close()
        f.close()
    


if __name__ == "__main__":

    QAlg=["CE","IQFT","BV","QRAM"] 
    path = os.getcwd()

    for name in QAlg:
        
        folderPath = f"{path}/{name}/{name}Mutants"
        adaptPath = folderPath + "Adapted/"
        PGZPath = folderPath + "PGZ/"
        
        os.mkdir(adaptPath)
        os.mkdir(PGZPath)
        
        adapt(folderPath, adaptPath, PGZPath)
        

