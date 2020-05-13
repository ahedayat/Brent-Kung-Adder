from .pg import PG as PG
from .bitwise_pg_logic import BitwisePGLogic as BitwisePGLogic
from .group_pg_logic import GroupPGLogic as GroupPGLogic
from .sum_logic import SumLogic as SumLogic
from .brent_kung_adder import BrentKungAdder as BrentKungAdder
from adders.blocks import BlackBlock
from adders.blocks import GrayBlock


def write_module(file_path, module):
    file_name = "{}.v".format(module.module_name)
    module.verilog(file_path=file_path, file_name=file_name)
    print('"{file_name}"'.format(file_name=file_name))


def write(file_path, bitwidth):
    print('Genrated:')
    # Write BlackBlock.v
    write_module(file_path, BlackBlock())

    # Write GrayBlock.v
    write_module(file_path, GrayBlock())

    # Write PG.v
    write_module(file_path, PG())

    # Write BitwisePGLogic.v
    write_module(file_path, BitwisePGLogic(bitwidth))

    # Write GroupPGLogic.v
    write_module(file_path, GroupPGLogic(bitwidth))

    # Write SumLogic.v
    write_module(file_path, SumLogic(bitwidth))

    # Write BrentKungAdder
    write_module(file_path, BrentKungAdder(bitwidth))
