import verilog as verilog


class SumLogic:
    module_name = 'SumLogic'

    def __init__(self, bitwidth):
        self.bitwidth = bitwidth

    def inputs(self):
        Ps = ['P_{}'.format(ix) for ix in range(self.bitwidth+1)]
        Gs = ['G_{}_0'.format(ix) for ix in range(self.bitwidth+1)]
        return Ps, Gs

    def outputs(self):
        Ss = ['S_{}'.format(ix) for ix in range(1, self.bitwidth+1)]
        c_out = 'C_out'
        return c_out, Ss

    def verilog(self, file_path, file_name):
        m = verilog.Module(SumLogic.module_name)

        Ps, Gs = self.inputs()
        c_out, Ss = self.outputs()

        for bit in range(1, self.bitwidth+1):
            # Comment
            m.comment('Bit {}'.format(bit))

            # Instantiation
            m.stmt_assign("S_{}".format(bit), "{g_im1_0} ^ {p_i}".format(
                g_im1_0="G_{}_0".format(bit-1),
                p_i="P_{}".format(bit)))

        # Carry
        m.comment('Carry Out')
        m.stmt_assign(c_out, 'G_{}_0'.format(self.bitwidth))

        for bit, (p, g) in enumerate(zip(Ps, Gs)):
            m.input(p, 'input')
            m.input(g, 'input')

        for s in Ss:
            m.output(s, 'output')
        m.output(c_out, 'output')

        m.start()

        m.end()

        m.write(file_path, file_name)

    def instantiation(self, instance_name, inputs, outputs):
        """
            inputs: dict{ port: ? , connector: ?}
            outputs: dict{ port: ? , connector: ?}
        """
        return verilog.Module.instantiate(module_name=SumLogic.module_name,
                                          instance_name=instance_name,
                                          inputs=inputs,
                                          outputs=outputs)
