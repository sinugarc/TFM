import os

def gateIncrease(original_path:str, num_increase:int, end_num_gate:int):
    
    incl=""
    for _ in range(num_increase):
        incl += "\nqc.h(q[5])"
    incl += "\n"
    
    num_qc = (end_num_gate - 25)//num_increase+1
    
    f = open(original_path,"r")
    text = f.read()
    f.close()
    
    auxPath = original_path[:-5]
    
    for i in range(num_qc):
        
        g = open(f"{auxPath}{25+(i+1)*num_increase}.py","w")
        text += incl
        g.write(text)
        g.close()
    
    
def adapt (folderPath: str, adaptPath:str, PGZPath:str):
    
    files = [f for f in os.listdir(folderPath) if os.path.isfile(os.path.join(folderPath,f)) and f[0]=="I"]

    for x in files:
        
        f = open(folderPath+"/"+x,"r")
        g = open(adaptPath+x,"w")

        g.write("import pickle\nimport gzip\n")
        g.write(f.read())
        g.write(f"\n\nwith gzip.open('{PGZPath}{x[:-3]}.pgz',mode='wb') as f:\n    pickle.dump(qc,f)\nf.close()")
        g.close()
        f.close()
        
if __name__ == "__main__":
    
    path = os.getcwd()
    
    gateIncrease(f"{path}/IQFT25.py",5,99)
    
    os.mkdir(f"{path}/adaptPath")
    os.mkdir(f"{path}/PGZPath")
    
    adapt(path, f"{path}/adaptPath/", f"{path}/PGZPath/")