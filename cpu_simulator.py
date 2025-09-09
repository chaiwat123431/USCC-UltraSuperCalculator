# USCC Ultra Super Calculator CPU Simulator

class UltraSuperCalculator:
    def __init__(self, name):
        self.name = name
        self.number_registers = [0] * 22
        self.history_registers = [0] * 10
        self.numbers_index = 1
        self.history_index = 0
        self.temp_history_index = 0
        self.user_display = ""
        self.update_display(f"Welcome to {self.name}'s Calculator!")

    def update_display(self, to_update):
        self.user_display = to_update
        print(self.user_display)

    # Store a binary value in the next available number register
    def store_value_to_register(self, value_to_store):
        if self.numbers_index > 21:
            self.numbers_index = 1
        self.number_registers[self.numbers_index] = int(value_to_store, 2)
        print(f"Value: {int(value_to_store,2)} stored in Register: {self.numbers_index}.")
        self.numbers_index += 1

    # Load value from a register by its binary address
    def load_value_from_register(self, register_address):
        index = int(register_address, 2)
        int_value = int(self.number_registers[index])
        return int_value

    # Store result in history buffer
    def store_to_history_register(self, result_to_store):
        if self.history_index > 9:
            self.history_index = 0
        self.history_registers[self.history_index] = bin(result_to_store)
        self.history_index += 1
        self.temp_history_index = self.history_index

    # ALU Operations
    def add(self, address_num1, address_num2):
        num1 = self.load_value_from_register(address_num1)
        num2 = self.load_value_from_register(address_num2)
        return num1 + num2

    def multiply(self, address_num1, address_num2):
        num1 = self.load_value_from_register(address_num1)
        num2 = self.load_value_from_register(address_num2)
        return num1 * num2

    def subtract(self, address_num1, address_num2):
        num1 = self.load_value_from_register(address_num1)
        num2 = self.load_value_from_register(address_num2)
        return num1 - num2

    def divide(self, address_num1, address_num2):
        num1 = self.load_value_from_register(address_num1)
        num2 = self.load_value_from_register(address_num2)
        if num2 == 0:
            print(f"Division by 0 error: {num1}/{num2}.")
            return 0
        return int(num1 / num2)

    # Retrieve last calculation from history
    def get_last_calculation(self):
        self.temp_history_index -= 1
        last_value = f"The last calculated value was: {int(self.history_registers[self.temp_history_index],2)}"
        self.update_display(last_value)

    # Read a 32-bit instruction and execute
    def binary_reader(self, instruction):
        if len(instruction) != 32:
            self.update_display("Invalid Instruction Length")
            return

        opcode = instruction[0:6]
        source_one = instruction[6:11]
        source_two = instruction[11:16]
        store = instruction[16:26]
        function_code = instruction[26:32]

        # OPCODE handling
        if opcode == '000001':  # Store value to register
            self.store_value_to_register(store)
            return
        elif opcode == '100001':  # Retrieve last calculation
            self.get_last_calculation()
            return
        elif opcode != '000000':  # Invalid
            self.update_display("Invalid OPCODE")
            return

        # ALU operations
        result = 0
        if function_code == '100000':  # ADD
            result = self.add(source_one, source_two)
        elif function_code == '100010':  # SUBTRACT
            result = self.subtract(source_one, source_two)
        elif function_code == '011000':  # MULTIPLY
            result = self.multiply(source_one, source_two)
        elif function_code == '011010':  # DIVIDE
            result = self.divide(source_one, source_two)
        else:
            self.update_display("Invalid FUNCTION CODE")
            return

        # Store result in history and display
        self.store_to_history_register(result)
        self.update_display(f"Result: {result}")


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    calc = UltraSuperCalculator("Chaiwat")

    # Store 10 in register
    calc.binary_reader("000001000000000000000000001010")  # 10 in binary

    # Store 5 in register
    calc.binary_reader("000001000000000000001010000101")  # 5 in binary

    # Add R1 + R2
    calc.binary_reader("000000000010001000000000100000")  # ADD function code

    # Subtract R1 - R2
    calc.binary_reader("000000000010001000000000100010")  # SUBTRACT function code

    # Multiply R1 * R2
    calc.binary_reader("000000000010001000000000011000")  # MULTIPLY function code

    # Divide R1 / R2
    calc.binary_reader("000000000010001000000000011010")  # DIVIDE function code

    # Show last calculation
    calc.binary_reader("100001000000000000000000000000")  # Retrieve last
