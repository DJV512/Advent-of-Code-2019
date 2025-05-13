import sys

class Intcode:

    def __init__(self, memory):
        self.memory = memory
        self.pointer = 0

        self.OPCODES = {
            1: self.add,
            2: self.multiply,
            3: self.user_input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equal,
            99: self.exit,
        }

    def parse_opcode(self):
        instruction = list(f"{self.memory[self.pointer]:04}")
        opcode = int("".join(instruction[-2:]))
        if opcode in [1,2,5,6,7,8]:
            param_modes = [int(instruction[-3]), int(instruction[-4])]
        elif opcode in [3,4]:
            param_modes = [int(instruction[-3])]
        elif opcode == 99:
            return 99, []
        else:
            raise ValueError(f"Unknown opcode {opcode}")
        return opcode, param_modes
    

    def get_params(self, param_modes):
        params = []
        for param_mode in param_modes:
            self.pointer += 1
            if param_mode == 0:
                params.append(self.memory[self.memory[self.pointer]])
            else:
                params.append(self.memory[self.pointer])
        return params
        
    
    def add(self, param_modes):
        params = self.get_params(param_modes)
        self.pointer += 1
        params.append(self.memory[self.pointer])
        self.memory[params[2]] = params[0] + params[1]
        self.pointer += 1
        

    def multiply(self, param_modes):
        params = self.get_params(param_modes)
        self.pointer += 1
        params.append(self.memory[self.pointer])
        self.memory[params[2]] = params[0] * params[1]
        self.pointer += 1

        
    def user_input(self, param_modes = None):
        while True:
            try:
                value = int(input("Please input a value: "))
            except:
                print("Please enter only numbers.")
            else:
                break
        self.memory[self.memory[self.pointer+1]] = value
        self.pointer += 2

    
    def output(self, param_modes):
        if param_modes[0] == 0:
            value = self.memory[self.memory[self.pointer+1]]
        else:
            value = self.memory[self.pointer+1]
        print(f"Output of instruction at pointer value {self.pointer} is {value}.")
        self.pointer += 2


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
        self.pointer += 1
        params.append(self.memory[self.pointer])

        if params[0] < params[1]:
            self.memory[params[2]] = 1
        else:
            self.memory[params[2]] = 0
        
        self.pointer += 1


    def equal(self, param_modes):
        params = self.get_params(param_modes)
        self.pointer += 1
        params.append(self.memory[self.pointer])

        if params[0] == params[1]:
            self.memory[params[2]] = 1
        else:
            self.memory[params[2]] = 0
        
        self.pointer += 1
        

    def exit(self, param_modes = None):
        self.pointer = float('inf')
        return

    
    def run(self):
        while self.pointer < len(self.memory):
            opcode, param_modes = self.parse_opcode()
            func = self.OPCODES[opcode]
            func(param_modes = param_modes)




def test():
    with open("Day2/input.txt") as f:
        day2 = [int(x) for x in f.read().strip().split(",")]
    day2[1] = 12
    day2[2] = 2
    print("Day 2 Memory[0] = 5434663")
    computer = Intcode(day2)
    computer.run()
    print(computer.memory[0]==5434663)
    print()


    print("Day 5 sample: Receive back whatever number you input.")
    day5sample = [3,0,4,0,99]
    computer = Intcode(day5sample)
    computer.run()
    print(computer.memory[0])
    print()
 

    day5part2sample = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
    print("Day 5 Part 2 Sample (Compare input to 8: 999 if less, 1000 if equal, 1001 if greater)")
    computer = Intcode(day5part2sample)
    computer.run()
    print()


    with open("Day5/input.txt") as f:
        day5 = [int(x) for x in f.read().strip().split(",")]
    print("Day 5 Diagnosis Codes:")
    print("Input 1 = 2845163")
    print("Input 5 = 9436229")
    computer = Intcode(day5)
    computer.run()

    

if __name__ == "__main__":
    test()