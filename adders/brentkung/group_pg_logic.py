import math
import utils as utils
import adders.blocks as blocks
import verilog as verilog


class GroupPGLogic:
    module_name = 'GroupPGLogic'

    def __init__(self, bitwidth):
        self.bitwidth = bitwidth + 1
        self.block_matrix = self.generate_block_matrix()
        self.row, self.col = len(self.block_matrix), len(self.block_matrix[0])

    def generate_block_matrix(self):
        height = int(2*math.log2(self.bitwidth) - 1)
        bmatrix = utils.create_matrix_2d(
            height, self.bitwidth, default_val=('|', None))

        # Upside
        pow2 = 1
        for ix in range(math.ceil(height/2)):
            pow2 *= 2
            prev_route = pow2/2
            for jx in range(self.bitwidth-1, -1, -1):
                if ((jx+1) % pow2) == 0:
                    if jx == math.pow(2, ix+1)-1:
                        bmatrix[ix][jx] = ('Gray', jx-prev_route)
                    else:
                        bmatrix[ix][jx] = ('Black', jx-prev_route)
                elif ((jx+1) % pow2) == (pow2/2):
                    bmatrix[ix][jx] = ('Buffer', None)
                else:
                    continue

        # Downside
        downside_start_index = math.ceil(height/2)
        pow2 /= 2
        for ix in range(downside_start_index, downside_start_index+math.floor(height/2)):
            for jx in range(self.bitwidth-1, -1, -1):
                if (jx+1) % pow2 == pow2/2:
                    if (jx+1+pow2/2) / pow2 != 1:
                        bmatrix[ix][jx] = ('Gray', jx-pow2/2)
                elif False and (jx+1) % pow2 == 0:
                    if (jx+1)/pow2 != 1:
                        bmatrix[ix][jx] = ('Buffer', None)
                else:
                    continue

            pow2 /= 2

        return bmatrix

    def height(self):
        return int(2*math.log2(self.bitwidth) - 1)

    def p_i_j(self, i, row):
        height = self.height()
        j = 0
        if row < math.ceil(height/2) and row <= math.log2(self.bitwidth):
            j = i-math.pow(2, row+1)+1
        if row >= math.ceil(height/2):
            j = i - math.pow(2, height-1-row)
        return 'P_{}_{}'.format(int(i), int(j))

    def g_i_j(self, i, row):
        height = self.height()
        j = 0
        if row < math.ceil(height/2) and row <= math.log2(self.bitwidth):
            j = i-math.pow(2, row+1)+1
        if row >= math.ceil(height/2):
            j = i - math.pow(2, height-1-row)
        return 'G_{}_{}'.format(int(i), int(j))

    def inputs(self):
        Ps = ['P_{}_{}'.format(ix, ix) for ix in range(self.bitwidth)]
        Gs = ['G_{}_{}'.format(ix, ix) for ix in range(self.bitwidth)]
        return Gs, Ps

    def outputs(self):
        Ps = ['P_{}_0'.format(ix, ix) for ix in range(self.bitwidth)]
        Gs = ['G_{}_0'.format(ix, ix) for ix in range(self.bitwidth)]
        return Gs, Ps

    def input_i_j(self, r, c):
        height = self.height()

        i = c
        if r < math.ceil(height/2):
            if r == 0:
                j = c
            else:
                j = c - math.pow(2, r) + 1
        else:
            if r == height-1:
                j = c
            else:
                j = c - math.pow(2, height-r-1) + 1
        return int(i), int(j)

    def output_i_j(self, r, c):
        height = self.height()

        i = c
        if r < math.ceil(height/2):
            j = c - math.pow(2, r+1) + 1
        else:
            j = 0
        return int(i), int(j)

    def black_block(self, r, c, block_in):
        # Inputs
        # print('---------------- Black Block ----------------')
        height = self.height()
        in1_i, in1_j = self.input_i_j(r, c)
        in2_i, in2_j = self.input_i_j(r, block_in)

        _g_i_k = verilog.Module.in_connector(
            'G_i_k', 'G_{}_{}'.format(in1_i, in1_j))
        _p_i_k = verilog.Module.in_connector(
            'P_i_k', 'P_{}_{}'.format(in1_i, in1_j))
        _g_km1_j = verilog.Module.in_connector(
            'G_km1_j', 'G_{}_{}'.format(in2_i, in2_j))
        _p_km1_j = verilog.Module.in_connector(
            'P_km1_j', 'P_{}_{}'.format(in2_i, in2_j))

        # Outputs
        out_i, out_j = self.output_i_j(r, c)
        _g_i_j = verilog.Module.out_connector(
            'G_i_j', 'G_{}_{}'.format(out_i, out_j))
        _p_i_j = verilog.Module.out_connector(
            'P_i_j', 'P_{}_{}'.format(out_i, out_j))

        inputs = [_g_i_k, _p_i_k, _g_km1_j, _p_km1_j]
        outputs = [_g_i_j, _p_i_j]

        i, j = c, self.p_i_j(c, r).split('_')[-1]
        if in1_i == in1_j or in2_i == in2_j:
            wires = [output['connector'] for output in outputs]
        elif out_j == 0:
            wires = [input['connector'] for input in inputs]
        else:
            wires = [input['connector'] for input in inputs] + \
                [output['connector'] for output in outputs]

        # print('#### Inputs')
        # print('r={}, c={}'.format(r, c))
        # print('_g_i_k={}'.format(_g_i_k))
        # print('_p_i_k={}'.format(_p_i_k))
        # print('_g_km1_j={}'.format(_g_km1_j))
        # print('_p_km1_j={}'.format(_p_km1_j))
        # print('#### Outputs')
        # print('_g_i_j={}'.format(_g_i_j))
        # print('_p_i_j={}'.format(_p_i_j))

        # import pdb
        # pdb.set_trace()

        return wires, blocks.BlackBlock.instantiation(instance_name='black_block_{}_{}'.format(i, j),
                                                      inputs=inputs,
                                                      outputs=outputs)

    def gray_block(self, r, c, block_in):
        # print('---------------- Gray Block ----------------')
        height = self.height()
        # Inputs
        in1_i, in1_j = self.input_i_j(r, c)
        in2_i, in2_j = self.input_i_j(r, block_in)
        if r >= math.ceil(height/2):
            in2_j = 0

        _g_i_k = verilog.Module.in_connector(
            'G_i_k', 'G_{}_{}'.format(in1_i, in1_j))
        _p_i_k = verilog.Module.in_connector(
            'P_i_k', 'P_{}_{}'.format(in1_i, in1_j))
        _g_km1_j = verilog.Module.in_connector(
            'G_km1_j', 'G_{}_{}'.format(in2_i, in2_j))

        # Outputs
        out_i, out_j = self.output_i_j(r, c)
        _g_i_j = verilog.Module.out_connector(
            'G_i_j', 'G_{}_{}'.format(out_i, out_j))

        inputs = [_g_i_k, _p_i_k, _g_km1_j]
        outputs = [_g_i_j]

        i, j = c, self.p_i_j(c, r).split('_')[-1]
        if r == 0:
            wires = [output['connector'] for output in outputs]
        elif r == height-1:
            wires = [input['connector'] for input in inputs]
        else:
            wires = [input['connector'] for input in inputs] + \
                [output['connector'] for output in outputs]

        return wires, blocks.GrayBlock.instantiation(instance_name='gray_block_{}_{}'.format(i, j),
                                                     inputs=inputs,
                                                     outputs=outputs)

    def verilog(self, file_path, file_name):
        m = verilog.Module(GroupPGLogic.module_name)

        all_wires = list()
        input_Gs, input_Ps = self.inputs()
        output_Gs, output_Ps = self.outputs()
        for r in range(self.row):
            for c in range(self.col):
                block_type, block_in = self.block_matrix[r][c]

                if block_type == 'Black' or block_type == 'Gray':
                    new_wires, new_block = None, None
                    if block_type == 'Black':
                        new_wires, new_block = self.black_block(r, c, block_in)
                    else:
                        new_wires, new_block = self.gray_block(r, c, block_in)

                    for wire in new_wires:
                        if wire not in all_wires:
                            all_wires.append(wire)

                    m.instruction(new_block)

                elif block_type == 'Buffer':
                    continue
                elif block_type == '|':
                    continue
                else:
                    exit()

        for wire in all_wires:
            if wire in (input_Gs + input_Ps + output_Gs + output_Ps):
                continue
            i, j = wire.split('_')[-2], wire.split('_')[-1]
            m.wire(wire, 'wire')

        for (p, g) in zip(input_Ps, input_Gs):
            m.input(p, 'input')
            m.input(g, 'input')

        for ix, (p, g) in enumerate(zip(output_Ps, output_Gs)):
            if ix == 0:
                m.output('_'+p, 'output')
                m.output('_'+g, 'output')
                m.stmt_assign('_'+p, p)
                m.stmt_assign('_'+g, g)
            else:
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
        return verilog.Module.instantiate(module_name=GroupPGLogic.module_name,
                                          instance_name=instance_name,
                                          inputs=inputs,
                                          outputs=outputs)
