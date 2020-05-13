from .pg import PG as PG
import verilog as verilog


class BitwisePGLogic:
    module_name = 'BitwisePGLogic'

    def __init__(self, bitwidth):
        self.bitwidth = bitwidth

    def inputs(self):
        c0 = "C_0"
        As = ['A_{}'.format(ix+1) for ix in range(self.bitwidth)]
        Bs = ['B_{}'.format(ix+1) for ix in range(self.bitwidth)]
        return c0, As, Bs

    def outputs(self):
        Ps = ['P_{}'.format(ix) for ix in range(self.bitwidth+1)]
        Gs = ['G_{}'.format(ix) for ix in range(self.bitwidth+1)]
        return Ps, Gs

    def pg_inputs(self, ix):
        a = {"port": "A_i",
             "connector": "A_{}".format(ix)}
        b = {"port": "B_i",
             "connector": "B_{}".format(ix)}
        return [a, b]

    def pg_outputs(self, ix):
        p = {"port": "P_i",
             "connector": "P_{}".format(ix)}
        g = {"port": "G_i",
             "connector": "G_{}".format(ix)}
        return [p, g]

    def verilog(self, file_path, file_name):
        m = verilog.Module(BitwisePGLogic.module_name)

        c0, input_As, input_Bs = self.inputs()
        output_Ps, output_Gs = self.outputs()

        for bit in range(self.bitwidth+1):
            # Comment
            m.comment('Bit {}'.format(bit))
            if bit == 0:
                m.stmt_assign("P_0", "0")
                m.stmt_assign("G_0", "C_0")

            else:
                # Instantiation
                _pg_inputs = self.pg_inputs(bit)
                _pg_outputs = self.pg_outputs(bit)
                new_pg = PG().instantiation(instance_name="PG_Bit_{}".format(bit),
                                            inputs=_pg_inputs, outputs=_pg_outputs)

                # Add Instruction
                m.instruction(new_pg)

        for (a, b) in zip(input_As, input_Bs):
            m.input(a, 'input')
            m.input(b, 'input')
        m.input(c0, 'input')

        for (p, g) in zip(output_Ps, output_Gs):
            m.output(p, 'output')
            m.output(g, 'output')

        m.start()

        m.end()

        m.write(file_path, file_name)

    def instantiation(self, instance_name, inputs, outputs):
        """
            inputs: dict{ port: ? , connector: ?}
            outputs: dict{ port: ? , connector: ?}
        """
        return verilog.Module.instantiate(module_name=BitwisePGLogic.module_name,
                                          instance_name=instance_name,
                                          inputs=inputs,
                                          outputs=outputs)
