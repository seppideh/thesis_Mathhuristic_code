def read_file(fileName):
    Vic = []
    CE = []
    CEr = []
    D = []
    Cap = []
    PC = []
    PCr = []
    SP = []
    FC = []
    with open(fileName, 'r') as file:
        line = file.readline()
        while line:
            numbers_list = line.split()
            numbers_list = [float(num) for num in numbers_list]
            if len(numbers_list)==2:
                Vic.append(numbers_list)
            line = file.readline()
            if line.strip()=="CE":
                line = file.readline()
                CE=line.split()
                continue
            if line.strip()=="CEr":
                line = file.readline()
                CEr=line.split()
                continue 
            if line.strip()=="D":
                line = file.readline()
                D=line.split()
                continue                
            if line.strip()=="Cap":
                line = file.readline()
                Cap=line.split()
                continue 
            if line.strip()=="PC":
                line = file.readline()
                PC=line.split()
                continue         
            if line.strip()=="PCr":
                line = file.readline()
                PCr=line.split()
                continue
            if line.strip()=="SP":
                line = file.readline()
                SP=line.split()
                continue 
            if line.strip()=="FC":
                line = file.readline()
                FC=line.split()
                continue
        CE=[float(x) for x in CE]
        CEr=[float(x) for x in CEr]
        D=[float(x) for x in D]
        Cap=[float(x) for x in Cap]
        PC=[float(x) for x in PC]
        PCr=[float(x) for x in PCr]
        SP=[float(x) for x in SP]
        FC=[float(x) for x in FC]
                

        return Vic,CE,CEr,D,Cap,PC,PCr,SP,FC
