import verilog as verilog


class PG:
    module_name = 'PG'

    def __init__(self):
        pass

    def inputs(self):
        return ['A_i', 'B_i']

    def outputs(self):
        return ['G_i', 'P_i']

    def verilog(self, file_path, file_name):
        m = verilog.Module(PG.module_name)

        # Inputs
        for input in self.inputs():
            m.input(input, 'input')
        # Outputs
        for output in self.outputs():
            m.output(output, 'output')

        # Start
        m.start()

        # Assignments
        m.stmt_assign('G_i', 'A_i & B_i')
        m.stmt_assign('P_i', 'A_i ^ B_i')

        # End
        m.end()

        # Write File
        m.write(file_path, file_name)

    def instantiation(self, instance_name, inputs, outputs):
        """
            inputs: [dict{ port: ? , connector: ?}]
            outputs: [dict{ port: ? , connector: ?}]
        """
        return verilog.Module.instantiate(module_name=PG.module_name,
                                          instance_name=instance_name,
                                          inputs=inputs,
                                          outputs=outputs)
