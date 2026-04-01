import shutil
import datetime
import os
 
def fazer_backup():
    if not os.path.exists("backup"):
        os.makedirs("backup")
 
    data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
 
    origem = "banco.db"     
    destino = f"backup/banco_{data}.db"
 
    if not os.path.exists(origem):
        print("Arquivo banco.db não encontrado!")
        return
 
    shutil.copy(origem, destino)
    print(f"Backup realizado: {destino}")