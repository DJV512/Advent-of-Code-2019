import sys
from copy import deepcopy

class Intcode:

    def __init__(self, memory, inputs=None, verbose=False, interactive=False):
        self.memory = deepcopy(memory)
        self.pointer = 0
        self.inputs = inputs or []
        self.outputs = []
        self.verbose = verbose
        self.interactive = interactive
        self.relative_base = 0
        self.halted = False

        self.OPCODES = {
            1: self.add,
            2: self.multiply,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equal,
            9: self.adjust_base,
            99: self.exit,
        }

        
    def parse_opcode(self):
        instruction = list(f"{self.memory[self.pointer]:05}")
        opcode = int("".join(instruction[-2:]))
        if opcode in [1,2,7,8]:
            param_modes = [int(instruction[-3]), int(instruction[-4]), int(instruction[-5])]
        elif opcode in [5,6]:
            param_modes = [int(instruction[-3]), int(instruction[-4])]
        elif opcode in [3,4,9]:
            param_modes = [int(instruction[-3])]
        elif opcode == 99:
            return 99, []
        else:
            raise ValueError(f"Unknown opcode {opcode} at memory position {self.pointer}.")
        return opcode, param_modes
    

    def get_params(self, param_modes):
        params = []
        for i, param_mode in enumerate(param_modes):
            self.pointer += 1
            if param_mode == 0 and i != 2:
                params.append(self.memory[self.memory[self.pointer]])
            elif param_mode == 0:
                params.append(self.memory[self.pointer])
            elif param_mode == 1:
                params.append(self.memory[self.pointer])
            elif param_mode == 2 and i != 2:
                params.append(self.memory[self.memory[self.pointer]+self.relative_base])
            elif param_mode == 2:
                params.append(self.memory[self.pointer]+self.relative_base)
        return params
        
    
    def add(self, param_modes):
        params = self.get_params(param_modes)
        self.memory[params[2]] = params[0] + params[1]
        self.pointer += 1
        

    def multiply(self, param_modes):
        params = self.get_params(param_modes)
        self.memory[params[2]] = params[0] * params[1]
        self.pointer += 1

        
    def input(self, param_modes = None):
        if self.verbose:
            print(f"INPUT called. Current inputs: {self.inputs}")
        if self.inputs:
            value = self.inputs.pop(0)
        elif self.interactive:
            while True:
                try:
                    value = int(input("Please input a value: "))
                except:
                    print("Please enter only numbers.")
                else:
                    break
        else:
            return "waiting"
        
        if param_modes[0] == 0:
            self.memory[self.memory[self.pointer+1]] = value
        elif param_modes[0] == 2:
            self.memory[self.memory[self.pointer+1]+self.relative_base] = value
        self.pointer += 2

    
    def output(self, param_modes):
        params = self.get_params(param_modes)
        value = params[0]
        if self.verbose:
            print(f"Output = {value}")
        self.outputs.append(value)
        self.pointer += 1
        return value


    def jump_if_true(self, param_modes):
        params = self.get_params(param_modes)
        
        if params[0] != 0:
            self.pointer = params[1]
        else:
            self.pointer += 1
    

    def jump_if_false(self, param_modes):
        params = self.get_params(param_modes)
        
        if params[0] == 0:
            self.pointer = params[1]
        else:
            self.pointer += 1
              

    def less_than(self, param_modes):
        params = self.get_params(param_modes)

        if params[0] < params[1]:
            self.memory[params[2]] = 1
        else:
            self.memory[params[2]] = 0
        
        self.pointer += 1


    def equal(self, param_modes):
        params = self.get_params(param_modes)

        if params[0] == params[1]:
            self.memory[params[2]] = 1
        else:
            self.memory[params[2]] = 0
        
        self.pointer += 1


    def adjust_base(self, param_modes):
        params = self.get_params(param_modes)
        self.relative_base += params[0]
        self.pointer += 1
        

    def exit(self, param_modes):
        self.pointer = float('inf')
        self.halted = True
        return

    
    def run(self):
        while self.pointer < len(self.memory):
            opcode, param_modes = self.parse_opcode()
            if self.verbose:
                print(f"{self.pointer=}, {self.relative_base=}, {opcode=}, {param_modes=}")
            func = self.OPCODES[opcode]
            result = func(param_modes = param_modes)

            if result is not None:
                yield result
    
    
    def run_without_halt(self):
        for _ in self.run():
            pass

    
    def clone(self):
        return deepcopy(self)




def test():
    from collections import defaultdict
    
    with open("Day2/input.txt") as f:
        day2 = [int(x) for x in f.read().strip().split(",")]
    day2[1] = 12
    day2[2] = 2
    print("Day 2 Memory[0] = 5434663")
    computer = Intcode(day2, interactive=True)
    computer.run_without_halt()
    print(computer.memory[0]==5434663)
    print()


    print("Day 5 sample: Receive back whatever number you input.")
    day5sample = [3,0,4,0,99]
    computer = Intcode(day5sample, interactive=True)
    computer.run_without_halt()
    print(computer.memory[0])
    print()
 

    day5part2sample = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    print("Day 5 Part 2 Sample (Compare input to 8: 999 if less, 1000 if equal, 1001 if greater)")
    computer = Intcode(day5part2sample, interactive=True)
    computer.run_without_halt()
    print(computer.outputs)
    print()


    with open("Day5/input.txt") as f:
        day5 = [int(x) for x in f.read().strip().split(",")]
    print("Day 5 Diagnosis Codes:")
    print("Input 1 = 2845163")
    print("Input 5 = 9436229")
    computer = Intcode(day5, interactive=True)
    computer.run_without_halt()
    print(computer.outputs)
    print()
    
    
    day9part1sample = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    day9part1dict = defaultdict(int)
    for i, item in enumerate(day9part1sample):
        day9part1dict[i] = item
    print("Day 9 Part 1 Sample:")
    print("Output should be [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]")
    computer = Intcode(day9part1dict)
    computer.run_without_halt()
    print(computer.outputs)
    print()

    

if __name__ == "__main__":
    test()