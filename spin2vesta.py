import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s","--seed",help="seedname for input .cell file",required=True)
parser.add_argument("-o","--out",help="seedname for output .vesta file (optional)")

class vesta_cellp:
    def __init__(self,params,angles):
        self.params = params
        self.angles = angles

    def __repr__(self):
        string = ""
        string += "CELLP\n  "
        for p in self.params:
            string += f"{p}  "
        for a in self.angles:
            string += f"{a}  "
        return string

class vesta_struc:
    def __init__(self,atoms,positions):
        self.atoms = atoms
        self.positions = positions

    def __repr__(self):
        string = ""
        string += "STRUC\n"
        for i in range(len(self.atoms)):
            string += f"  {i+1} {self.atoms[i]}    {self.atoms[i]}    1.0000  "
            string += f"{self.positions[i][0]}  {self.positions[i][1]}  {self.positions[i][2]}    1a    1\n"
            string += "0.000000   0.000000   0.000000  0.00\n"
        string += "0 0 0 0 0 0 0"
        return string

class vesta_vectr:
    def __init__(self,vectors):
        self.vectors = vectors

    def __repr__(self):
        string = ""
        string += "VECTR\n"
        for i in range(len(self.vectors)):
            string += f"  {i+1}  {self.vectors[i][0]}  {self.vectors[i][1]}  {self.vectors[i][2]} 0\n"
            string += f"    {i+1}  0  0  0  0\n"
            string += "  0 0 0 0 0\n"
        string += "0 0 0 0 0\n0 0 0 0 0"
        return string

class vesta_vectt:
    def __init__(self,count,colours=None):
        self.count = count
        self.colours = colours

    def __repr__(self):
        string = ""
        string += "VECTT\n"
        for i in range(self.count):
            string += f"  {i+1}  0.500 "
            if not self.colours:
                string += f"255   0   0 "
            else:
                string += f"{self.colours[i][0]} {self.colours[i][1]} {self.colours[i][2]} "
            string += "1\n"
        string += "  0 0 0 0 0"
        return string


class castep_lattice_abc:
    def __init__(self,data):
        self.data = data
        self.params = []
        self.angles = []
        self.parse()

    def parse(self):
        self.params = list(map(float,self.data[0].split()))
        self.angles = list(map(float,self.data[1].split()))

class castep_positions_frac:
    def __init__(self,data):
        self.data = data
        self.atoms = []
        self.positions = []
        self.vectors = []
        self.parse()

    def parse(self):
        for line in self.data:
            sep = line.split()
            self.atoms.append(sep[0])
            self.positions.append(list(map(float,sep[1:4])))
            self.vectors.append(list(map(float,sep[5:8])))

castep_block = {"LATTICE_ABC": castep_lattice_abc,
                "POSITIONS_FRAC": castep_positions_frac}

def read_castep(fname):
    with open(f"{fname}.cell","r") as file:
        data = [line.strip() for line in file.readlines()]
    keyword = ""
    data_block = []
    castep_objs = {}
    for line in data:
        if "%" in line and line.upper().split()[0]=="%BLOCK":
            keyword = line.upper().split()[1] 
            data_block = []
        elif "%" in line and line.upper().split()[0]=="%ENDBLOCK":
            if keyword in castep_block.keys():
                obj = castep_block[keyword](data_block)
                castep_objs[keyword] = obj
        else:
            data_block.append(line)
    return castep_objs     

def castep_to_vesta(castep_objs):
    cellp = vesta_cellp(castep_objs["LATTICE_ABC"].params,castep_objs["LATTICE_ABC"].angles)
    struc = vesta_struc(castep_objs["POSITIONS_FRAC"].atoms,castep_objs["POSITIONS_FRAC"].positions)
    vectr = vesta_vectr(castep_objs["POSITIONS_FRAC"].vectors)
    vectt = vesta_vectt(len(castep_objs["POSITIONS_FRAC"].vectors))
    vesta_objs = [cellp,struc,vectr,vectt]
    return vesta_objs

def write_vesta(f_out,vesta_objs):
    with open(f"{f_out}.vesta","w") as file:
        file.write("MAGNETIC_CRYSTAL\n\n")
        for obj in vesta_objs:
            file.write(repr(obj))
            file.write("\n")

def convert(f_in,f_out):
    castep_objs = read_castep(f_in)
    vesta_objs = castep_to_vesta(castep_objs)
    write_vesta(f_out,vesta_objs)

if __name__=="__main__":
    args = parser.parse_args()
    f_in = args.seed
    if args.out:
        f_out = args.out
    else:
        f_out = f"{f_in}_vectors"
    convert(f_in,f_out)
