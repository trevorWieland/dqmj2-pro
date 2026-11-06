#include "context.h"
u8 native_main_02047428(const u8 *input)
{
    int opcode = *input;
    u8 used = 1;
    u16 *target = native_data_020fae64 + native_data_020fb264.field80;
    ++used;
    switch (opcode) {
    case 0x21:
        break;
    case 0x22:
        used += native_fn_02047ac0(0);
        break;
    case 0x24:
        used += native_fn_02047ac0(32);
        break;
    case 0x28:
        used += native_fn_02047b90(target, 0, 0, 255);
        break;
    case 0x2b:
        used += native_fn_02047b90(target, 1, 0, 255);
        break;
    case 0x2a:
        used += native_fn_02047b90(target, 2, 0, 255);
        break;
    case 0x29:
        used += native_fn_02047b90(target, 0, 1, 255);
        break;
    case 0x2d:
        used += native_fn_02047b90(target, 1, 1, 255);
        break;
    case 0x2c:
        used += native_fn_02047b90(target, 2, 1, 255);
        break;
    case 0x92:
        used += native_fn_02047b90(target, 1, 0, 0);
        break;
    case 0x93:
        used += native_fn_02047b90(target, 1, 0, 1);
        break;
    case 0x94:
        used += native_fn_02047b90(target, 1, 0, 2);
        break;
    case 0x95:
        used += native_fn_02047b90(target, 1, 0, 3);
        break;
    case 0x9a:
        used += native_fn_02047b90(target, 1, 1, 0);
        break;
    case 0x9b:
        used += native_fn_02047b90(target, 1, 1, 1);
        break;
    case 0x9c:
        used += native_fn_02047b90(target, 1, 1, 2);
        break;
    case 0x9d:
        used += native_fn_02047b90(target, 1, 1, 3);
        break;
    case 0x8e:
        used += native_fn_02047b90(target, 2, 0, 0);
        break;
    case 0x8f:
        used += native_fn_02047b90(target, 2, 0, 1);
        break;
    case 0x90:
        used += native_fn_02047b90(target, 2, 0, 2);
        break;
    case 0x91:
        used += native_fn_02047b90(target, 2, 0, 3);
        break;
    case 0x96:
        used += native_fn_02047b90(target, 2, 1, 0);
        break;
    case 0x97:
        used += native_fn_02047b90(target, 2, 1, 1);
        break;
    case 0x98:
        used += native_fn_02047b90(target, 2, 1, 2);
        break;
    case 0x99:
        used += native_fn_02047b90(target, 2, 1, 3);
        break;
    case 0x38:
        used += native_fn_02047bfc(target, 0, 0, 255);
        break;
    case 0x39:
        used += native_fn_02047bfc(target, 0, 1, 255);
        break;
    case 0x3b:
        used += native_fn_02047bfc(target, 1, 0, 255);
        break;
    case 0x3a:
        used += native_fn_02047bfc(target, 2, 0, 255);
        break;
    case 0x3d:
        used += native_fn_02047bfc(target, 1, 1, 255);
        break;
    case 0x3c:
        used += native_fn_02047bfc(target, 2, 1, 255);
        break;
    case 0xa2:
        used += native_fn_02047bfc(target, 1, 0, 0);
        break;
    case 0xa3:
        used += native_fn_02047bfc(target, 1, 0, 1);
        break;
    case 0xa4:
        used += native_fn_02047bfc(target, 1, 0, 2);
        break;
    case 0xa5:
        used += native_fn_02047bfc(target, 1, 0, 3);
        break;
    case 0x9e:
        used += native_fn_02047bfc(target, 2, 0, 0);
        break;
    case 0x9f:
        used += native_fn_02047bfc(target, 2, 0, 1);
        break;
    case 0xa0:
        used += native_fn_02047bfc(target, 2, 0, 2);
        break;
    case 0xa1:
        used += native_fn_02047bfc(target, 2, 0, 3);
        break;
    case 0xaa:
        used += native_fn_02047bfc(target, 1, 1, 0);
        break;
    case 0xab:
        used += native_fn_02047bfc(target, 1, 1, 1);
        break;
    case 0xac:
        used += native_fn_02047bfc(target, 1, 1, 2);
        break;
    case 0xad:
        used += native_fn_02047bfc(target, 1, 1, 3);
        break;
    case 0xa6:
        used += native_fn_02047bfc(target, 2, 1, 0);
        break;
    case 0xa7:
        used += native_fn_02047bfc(target, 2, 1, 1);
        break;
    case 0xa8:
        used += native_fn_02047bfc(target, 2, 1, 2);
        break;
    case 0xa9:
        used += native_fn_02047bfc(target, 2, 1, 3);
        break;
    }
    return used;
}
