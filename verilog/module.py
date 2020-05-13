

class Module:
    def __init__(self, module_name):
        self.start_instructions = list()
        self.instructions = list()
        self.end_instructions = list()
        self.module_name = module_name
        self.inputs = list()
        self.outputs = list()
        self.wires = list()
        pass

    def input(self, name, _type):
        self.inputs.append({
            'name': name,
            'type': _type,
        })

    def output(self, name, _type):
        self.outputs.append({
            'name': name,
            'type': _type,
        })

    def wire(self, name, _type):
        self.wires.append({
            'name': name,
            'type': _type
        })

    def start(self):
        ports = self.inputs+self.outputs

        # print(ports)

        module = 'module {} ( {} );'.format(
            self.module_name, ','.join(map(lambda x: x['name'], ports)))
        self.start_instructions.append(module)

        for input in self.inputs:
            self.start_instructions.append(
                '{} {};'.format(input['type'], input['name']))

        for output in self.outputs:
            self.start_instructions.append(
                '{} {};'.format(output['type'], output['name']))

        for wire in self.wires:
            self.start_instructions.append(
                '{} {};'.format(wire['type'], wire['name']))

    def end(self):
        self.end_instructions.append('endmodule')

    def stmt_assign(self, lhs, rhs):
        self.instructions.append('assign {} = {} ;'.format(lhs, rhs))

    def instruction(self, instruction):
        self.instructions.append(instruction)

    def comment(self, c):
        self.instructions.append('// {}'.format(c))

    def write(self, file_path, filename):
        all_instructions = self.start_instructions + \
            self.instructions + self.end_instructions
        with open('{}/{}'.format(file_path, filename), 'w') as f:
            for insts in all_instructions:
                f.write('{}\n'.format(insts))

    def __str__(self):
        return '\n'.join(self.instructions)

    @staticmethod
    def instantiate(module_name, instance_name, inputs, outputs):
        """
            inputs: [dict{ port: ? , connector: ?}]
            outputs: [dict{ port: ? , connector: ?}]
        """
        # Ports
        ports = inputs + outputs
        ports = ['.{port}({connector})'.format(
            port=port['port'], connector=port['connector']) for port in ports]
        ports = ','.join(ports)

        # Instruction
        instruction = '{module_name} {instance_name}({ports});'.format(
            module_name=module_name, instance_name=instance_name, ports=ports)

        return instruction

    @staticmethod
    def in_connector(port, connector):
        return {
            'port': port,
            'connector': connector
        }

    @staticmethod
    def out_connector(port, connector):
        return {
            'port': port,
            'connector': connector
        }
