typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_020414c8();
extern u32 native_fn_02041538();
extern u32 native_fn_02041814();
extern u32 native_fn_0205e844();
extern u32 native_fn_02061260();
extern u32 native_fn_020629e0();
extern u32 native_fn_020642cc();
extern u32 native_fn_020642f8();
extern u32 native_fn_02067b64();
extern u32 native_fn_020c40f4();
extern u32 native_fn_020cf43c();
extern u32 native_fn_020cf44c();
extern u32 native_fn_ov006_021d77d8();
extern u32 native_fn_ov006_021d77e8();
extern u32 native_fn_ov006_021d85c8();
extern u32 native_fn_ov006_021dcd30();
extern u32 native_fn_ov006_021dcd40();
extern u32 native_fn_ov006_021dd5cc();
extern u32 native_fn_ov006_021ded04();
extern u32 native_fn_ov006_021ded5c();
extern u32 native_fn_ov006_021dee68();
extern u32 native_fn_ov006_021def04();
extern u32 native_fn_ov006_021def28();
extern u32 native_fn_ov006_021df150();
extern u32 native_fn_ov006_021df16c();
extern u32 native_fn_ov006_021df590();
extern u8 native_data_ov006_0220f4e0[];
u32 native_ov006_021dcfec(void) {
    u8 temp_r0;
    u32 var_r4;

    var_r4 = 4;
    switch (*(u32 *)native_data_ov006_0220f4e0) {
    default:
        break;
    case 0:
        if (native_fn_0205e844(0x40) != 0) {
            native_fn_ov006_021dcd30(1);
            native_fn_ov006_021def28(0);
        }
        break;
    case 1:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dcd30(0xB);
        }
        break;
    case 3:
        if (native_fn_0205e844(0x40) != 0) {
            native_fn_ov006_021dcd30(4);
            native_fn_ov006_021def28(0);
        }
        break;
    case 2:
        native_fn_ov006_021def04();
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 1) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            if (native_fn_ov006_021df16c() == 0) {
                native_fn_ov006_021dcd30(5);
            } else {
                native_fn_ov006_021dcd40();
                native_fn_ov006_021ded5c(0xF, 4, 0x40);
                native_fn_ov006_021dcd30(0xA);
            }
        }
        break;
    case 4:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dcd30(5);
        }
        break;
    case 5:
        if (native_fn_020629e0() == 0x64) {
            native_fn_ov006_021ded04(0xF, 4, 0xF);
            native_fn_ov006_021dcd30(9);
        } else {
            native_fn_ov006_021dcd30(6);
        }
        break;
    case 9:
        native_fn_ov006_021def04();
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 1) {
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dee68();
            if (native_fn_ov006_021df16c() == 0) {
                native_fn_020642cc(0x20);
                native_fn_020c40f4(1);
                native_fn_020cf44c(0xF);
                native_fn_020cf43c(3);
                native_fn_ov006_021d77d8(0x10);
                native_fn_ov006_021dcd30(0xC);
                native_fn_020414c8(0x3F);
                native_fn_02041538(1, 2, 0xA);
            } else {
                native_fn_ov006_021dcd40();
                native_fn_ov006_021ded5c(0xF, 4, 0x40);
                native_fn_ov006_021dcd30(0xA);
            }
        }
        break;
    case 6:
        native_fn_ov006_021dd5cc(1);
        var_r4 = 1;
        native_fn_ov006_021d77e8(3);
        native_fn_020642cc(0x2C);
        break;
    case 7:
        native_fn_ov006_021dd5cc(2);
        var_r4 = 1;
        native_fn_ov006_021d77e8(3);
        native_fn_020642cc(0x2C);
        break;
    case 8:
        native_fn_02061260(1);
        
    case 10:
        if (M2C_FIELD((void *) native_fn_ov006_021df150(), u16 *, 2) & 0xFF7) {
            native_fn_ov006_021dee68();
            native_fn_ov006_021df590(0x52);
            native_fn_ov006_021dcd30(0xB);
        }
        break;
    case 11:
        temp_r0 = M2C_FIELD((void *) native_fn_020642f8(), u8 *, 4);
        switch (temp_r0) {
        default:
            break;
        case 0:
            native_fn_020642cc(0x24);
            native_fn_ov006_021d85c8(9);
            var_r4 = 3;
            break;
        case 1:
            native_fn_020642cc(0x24);
            native_fn_ov006_021d85c8(0x18);
            var_r4 = 3;
            break;
        case 2:
            native_fn_020642cc(0x24);
            native_fn_ov006_021d85c8(0x2F);
            var_r4 = 3;
            break;
        case 5:
        case 6:
            native_fn_020642cc(0x25);
            var_r4 = 5;
            break;
        case 9:
            native_fn_020642cc(0x26);
            var_r4 = 0;
            break;
        case 3:
        case 4:
        case 10:
            native_fn_ov006_021d77d8(9);
            native_fn_020414c8(0x3F);
            native_fn_02041538(1, 2, 0xA);
            native_fn_ov006_021dcd30(0xC);
            native_fn_020642cc(*(s32 *) native_fn_02067b64());
            break;
        case 7:
        case 8:
            native_fn_ov006_021d77d8(8);
            native_fn_020414c8(0x3F);
            native_fn_02041538(1, 2, 0xA);
            native_fn_ov006_021dcd30(0xC);
            native_fn_020642cc(0x33);
            break;
        }
        break;
    case 12:
        if (native_fn_02041814() != 1) {
            var_r4 = 6;
        }
        break;
    }
    return var_r4;
}
