import verilog as verilog

from .bitwise_pg_logic import BitwisePGLogic as BitwisePGLogic
from .group_pg_logic import GroupPGLogic as GroupPGLogic
from .sum_logic import SumLogic as SumLogic


class BrentKungAdder:
    module_name = 'BrentKungAdder'

    def __init__(self, bitwidth):
        self.bitwidth = bitwidth

    def inputs(self):
        As = ['A_{}'.format(ix+1) for ix in range(self.bitwidth)]
        Bs = ['B_{}'.format(ix+1) for ix in range(self.bitwidth)]
        c_in = 'C_0'
        return As, Bs, c_in

    def outputs(self):
        Ss = ['S_{}'.format(ix+1) for ix in range(self.bitwidth)]
        c_out = 'C_out'
        return c_out, Ss

    def bitwise_pg_logic_inputs(self):
        inputs = list()
        for bit in range(self.bitwidth+1):
            if bit == 0:
                c_in = {"port": "C_0",
                        "connector": "C_0"}
                inputs.append(c_in)
            else:
                _input_a = {"port": "A_{}".format(bit),
                            "connector": "A_{}".format(bit)}
                _input_b = {"port": "B_{}".format(bit),
                            "connector": "B_{}".format(bit)}
                inputs.append(_input_a)
                inputs.append(_input_b)
        return inputs

    def bitwise_pg_logic_outputs(self):
        outputs = list()
        for bit in range(self.bitwidth+1):
            _output_p = {"port": "P_{}".format(bit),
                         "connector": "P_{}".format(bit)}
            _output_g = {"port": "G_{}".format(bit),
                         "connector": "G_{}".format(bit)}
            outputs.append(_output_p)
            outputs.append(_output_g)

        return outputs

    def group_pg_logic_inputs(self):
        inputs = list()
        for bit in range(self.bitwidth+1):
            _input_p = {"port": "P_{}_{}".format(bit, bit),
                        "connector": "P_{}".format(bit, bit)}
            _input_g = {"port": "G_{}_{}".format(bit, bit),
                        "connector": "G_{}".format(bit, bit)}
            inputs.append(_input_p)
            inputs.append(_input_g)
        return inputs

    def group_pg_logic_outputs(self):
        outputs = list()
        for bit in range(self.bitwidth+1):
            if bit == 0:
                _output_p = {"port": "_P_{}_0".format(bit),
                             "connector": "P_{}_0".format(bit)}
                _output_g = {"port": "_G_{}_0".format(bit),
                             "connector": "G_{}_0".format(bit)}
            else:
                _output_p = {"port": "P_{}_0".format(bit),
                             "connector": "P_{}_0".format(bit)}
                _output_g = {"port": "G_{}_0".format(bit),
                             "connector": "G_{}_0".format(bit)}
            outputs.append(_output_p)
            outputs.append(_output_g)

        return outputs

    def sum_logic_inputs(self):
        inputs = list()
        for bit in range(self.bitwidth+1):
            _input_p = {"port": "P_{}".format(bit),
                        "connector": "P_{}".format(bit)}
            _input_g = {"port": "G_{}_0".format(bit),
                        "connector": "G_{}_0".format(bit)}
            inputs.append(_input_p)
            inputs.append(_input_g)
        return inputs

    def sum_logic_outputs(self):
        outputs = list()
        for bit in range(self.bitwidth):
            _output_s = {"port": "S_{}".format(bit+1),
                         "connector": "S_{}".format(bit+1)}
            outputs.append(_output_s)

        c_out = {"port": "C_out",
                 "connector": "C_out"}
        outputs.append(c_out)

        return outputs

    def add_new_wires(self, prev_wires, new_wires):
        for w in new_wires:
            if w['connector'] not in prev_wires:
                prev_wires.append(w['connector'])
        return prev_wires

    def add_module(self, m, module, instance_name, inputs, outputs, wires):
        instance = module.instantiation(
            instance_name=instance_name, inputs=inputs, outputs=outputs)

        m.instruction(instance)

        wires = self.add_new_wires(wires, inputs)
        wires = self.add_new_wires(wires, outputs)

        return m, wires

    def verilog(self, file_path, file_name):
        m = verilog.Module(BrentKungAdder.module_name)
        wires = list()

        input_As, input_Bs, c0 = self.inputs()
        c_out, Ss = self.outputs()

        # Instantiate Bitwise PG Logic
        bitwise_pg_logic_inputs = self.bitwise_pg_logic_inputs()
        bitwise_pg_logic_outputs = self.bitwise_pg_logic_outputs()

        m, wires = self.add_module(m=m,
                                   module=BitwisePGLogic(self.bitwidth),
                                   instance_name="_BitwisePGLogic",
                                   inputs=bitwise_pg_logic_inputs,
                                   outputs=bitwise_pg_logic_outputs,
                                   wires=wires)

        # Instantiate Group PG Logic
        group_pg_logic_inputs = self.group_pg_logic_inputs()
        group_pg_logic_outputs = self.group_pg_logic_outputs()

        m, wires = self.add_module(m=m,
                                   module=GroupPGLogic(self.bitwidth),
                                   instance_name="_GroupPGLogic",
                                   inputs=group_pg_logic_inputs,
                                   outputs=group_pg_logic_outputs,
                                   wires=wires)

        # Instantiate Sum Logic
        sum_logic_inputs = self.sum_logic_inputs()
        sum_logic_outputs = self.sum_logic_outputs()

        m, wires = self.add_module(m=m,
                                   module=SumLogic(self.bitwidth),
                                   instance_name="_SumLogic",
                                   inputs=sum_logic_inputs,
                                   outputs=sum_logic_outputs,
                                   wires=wires)

        # Inputs
        for (a, b) in zip(input_As, input_Bs):
            m.input(a, 'input')
            m.input(b, 'input')
        m.input(c0, 'input')

        # Outputs
        for (s) in Ss:
            m.output(s, 'output')
        m.output(c_out, 'output')

        # Wires
        ports = [c_out, c0] + Ss + input_As + input_Bs
        for wire in wires:
            if wire not in ports:
                m.wire(wire, 'wire')

        m.start()

        m.end()

        m.write(file_path, file_name)

    def instantiation(self, instance_name, inputs, outputs):
        """
            inputs: dict{ port: ? , connector: ?}
            outputs: dict{ port: ? , connector: ?}
        """
        return verilog.Module.instantiate(module_name=BrentKungAdder.module_name,
                                          instance_name=instance_name,
                                          inputs=inputs,
                                          outputs=outputs)
