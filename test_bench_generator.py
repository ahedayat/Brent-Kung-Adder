


def define_regs_wires(f, bitwidth):
    f.write('\treg[{}:0] s_golden;'.format(bitwidth))
    new_line(f)
    f.write('\treg[{}:1] a,b;'.format(bitwidth))
    new_line(f)
    f.write('\treg c_in;')
    new_line(f)
    f.write('\twire[{}:1] s;'.format(bitwidth))
    new_line(f)


def instantiation(f, bitwidth):
    instance = '\tBrentKungAdder adder('
    new_line(f)
    for bit in range(1, bitwidth+1):
        if bit==1:
            instance += '\n'
        instance += '{}.A_{}(a[{}]), .B_{}(b[{}]),\n'.format('\t' *
                                                             7, bit, bit, bit, bit)
    instance += '{}.C_0(c_in),\n'.format('\t'*7)
    for bit in range(1, bitwidth+1):
        if bit %2 == 1:
            instance += '{}'.format('\t'*7)
        instance += '.S_{}(s[{}]), '.format( bit, bit)
        if bit % 2 == 0:
            instance += '\n'
    instance += "{}.C_out(c_out));".format('\t'*7)
    f.write(instance)
    new_line(f)


def always_s_golden(f):
    f.write('\talways @(a,b,c_in) begin')
    new_line(f)
    f.write('\t\ts_golden = a + b + c_in;')
    new_line(f)
    f.write('\tend')
    new_line(f)
    new_line(f)


def initial(f, bitwidth, num_samples, a_samples, b_samples, delay=100):
    f.write('\tinitial begin')
    new_line(f)
    for sample in range(1,num_samples+1):
        f.write("\t\tc_in = 1'b0;")
        new_line(f)
        f.write("\t\ta = {};".format(a_samples[sample-1]))
        new_line(f)
        f.write("\t\tb = {};".format(b_samples[sample-1]))
        new_line(f)
        f.write('\t\t#{}'.format(delay))
        new_line(f)
        f.write('\t\t$display("================================================================================================================");')
        new_line(f)
        f.write('\t\t$display("In_1 = %d, In_2 = %d, c_in = %b, c_out = %b, My_Result = %d, Golden_Result = %d",a, b, c_in, c_out, s, s_golden);')
        new_line(f)
        if sample==num_samples:
            f.write('\t\t$display("================================================================================================================");')
            new_line(f)
        f.write('\t\t#{};'.format(delay))
        new_line(f)

    f.write('\tend')
    new_line(f)

def new_line(f):
    f.write('\n')


def _main():
    file_path = './outputs/64'
    file_name = 'test.v'
    bitwidth = 64
    num_samples = 2
    delay = 100

    a_samples = ["{}'b0011".format(bitwidth), "{}'b0101".format(bitwidth)]
    b_samples = ["{}'b0001".format(bitwidth), "{}'b1100".format(bitwidth)]


    with open('{}/{}'.format(file_path, file_name), 'w') as f:
        f.write('module test();\n')
        define_regs_wires(f, bitwidth)
        instantiation(f, bitwidth)
        always_s_golden(f)
        initial(f, bitwidth, num_samples, a_samples, b_samples, delay=delay)
        f.write('endmodule')


if __name__ == "__main__":
    _main()
