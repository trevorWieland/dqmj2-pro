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
extern u32 native_fn_020044ac();
extern u32 native_fn_020045d8();
extern u32 native_fn_0203d934();
extern u32 native_fn_0203d96c();
extern u32 native_fn_0203db28();
extern u32 native_fn_0203dc44();
extern u32 native_fn_0203dd70();
extern u32 native_fn_0203df6c();
extern u32 native_fn_0203e0c4();
extern u32 native_fn_0203e120();
extern u32 native_fn_0203e160();
extern u32 native_fn_0203e210();
extern u32 native_fn_0203e2dc();
extern u32 native_fn_0203e464();
extern u32 native_fn_0203e55c();
extern u32 native_fn_0203e990();
extern u32 native_fn_0203ea2c();
extern u32 native_fn_0203eb30();
extern u32 native_fn_0203eb5c();
extern u32 native_fn_0203ec74();
extern u32 native_fn_0203ecf4();
extern u32 native_fn_0203ed54();
extern u32 native_fn_0203ed74();
extern u32 native_fn_0203edf8();
extern u32 native_fn_0203ee7c();
extern u32 native_fn_0203ef34();
extern u32 native_fn_0203efa0();
extern u32 native_fn_0203f0a4();
extern u32 native_fn_0203f130();
extern u32 native_fn_0203f1ec();
extern u32 native_fn_0203f2b0();
extern u32 native_fn_0203f348();
extern u32 native_fn_0203f3a8();
extern u32 native_fn_0203f400();
extern u32 native_fn_0203f4b0();
extern u32 native_fn_0203f5b4();
extern u32 native_fn_0203f710();
extern u32 native_fn_0203f864();
extern u32 native_fn_0203f9a4();
extern u32 native_fn_0203f9e8();
extern u32 native_fn_0203fb98();
extern u32 native_fn_0203fc04();
extern u32 native_fn_0203fc80();
extern u32 native_fn_0203fcec();
extern u32 native_fn_0203fe60();
extern u32 native_fn_0203feb4();
extern u32 native_fn_0203ff14();
extern u32 native_fn_0203ffdc();
extern u32 native_fn_02041764();
extern u8 native_data_020f6054[];
u32 native_main_02040000(void) {
    u32 var_r8;
    u32 var_r9;

    var_r8 = 1;
    var_r9 = 1;
    native_fn_020044ac();
    native_fn_020045d8();
    do {
        switch (M2C_FIELD(native_data_020f6054, s8 *, 0xA)) {
        default:
            break;
        case 0x0:
            var_r8 = native_fn_0203d934();
            break;
        case 0x1:
            var_r8 = native_fn_0203db28();
            break;
        case 0x2:
            var_r8 = native_fn_0203dc44();
            break;
        case 0x3:
            var_r8 = native_fn_0203dd70();
            break;
        case 0x4:
            native_fn_0203df6c();
            var_r8 = 0;
            break;
        case 0x5:
            var_r8 = native_fn_0203e0c4();
            break;
        case 0xA:
            native_fn_0203e120();
            var_r8 = 0;
            break;
        case 0xB:
            native_fn_0203e210();
            var_r8 = 0;
            break;
        case 0xC:
            native_fn_0203e160();
            var_r8 = 0;
            break;
        case 0x12:
            native_fn_0203e990();
            var_r8 = 0;
            break;
        case 0x13:
            native_fn_0203eb30();
            var_r8 = 0;
            break;
        case 0x14:
            native_fn_0203ea2c(1);
            var_r8 = 0;
            break;
        case 0x15:
            native_fn_0203ea2c(0);
            var_r8 = 0;
            break;
        case 0x1E:
            native_fn_0203eb5c();
            var_r8 = 0;
            break;
        case 0x1F:
            native_fn_0203f400();
            var_r8 = 0;
            break;
        case 0x16:
            native_fn_0203ec74();
            var_r8 = 0;
            break;
        case 0x17:
            var_r8 = native_fn_0203ecf4();
            break;
        case 0x18:
            var_r8 = native_fn_0203ed54();
            break;
        case 0x19:
            native_fn_0203ed74();
            var_r8 = 0;
            break;
        case 0x1A:
            native_fn_0203edf8();
            var_r8 = 0;
            break;
        case 0x1C:
            native_fn_0203ef34();
            var_r8 = 0;
            break;
        case 0x1B:
            native_fn_0203ee7c();
            var_r8 = 0;
            break;
        case 0x31:
            native_fn_0203efa0();
            var_r8 = 0;
            break;
        case 0xD:
            native_fn_0203f0a4();
            var_r8 = 0;
            break;
        case 0xE:
            var_r9 = native_fn_0203f130();
            var_r8 = 0;
            break;
        case 0x6:
            var_r9 = native_fn_0203f9e8();
            var_r8 = 0;
            break;
        case 0x7:
            var_r9 = native_fn_0203fb98();
            var_r8 = 0;
            break;
        case 0x8:
            var_r9 = native_fn_0203fc04();
            var_r8 = 0;
            break;
        case 0x9:
            var_r9 = native_fn_0203fc80();
            var_r8 = 0;
            break;
        case 0xF:
            var_r9 = native_fn_0203f2b0();
            var_r8 = 0;
            break;
        case 0x10:
            native_fn_0203f348();
            var_r8 = 0;
            break;
        case 0x11:
            var_r9 = native_fn_0203f3a8();
            var_r8 = 0;
            break;
        case 0x20:
            native_fn_0203fe60();
            var_r8 = 0;
            break;
        case 0x21:
            native_fn_0203feb4();
            var_r8 = 0;
            break;
        case 0x1D:
            native_fn_0203fcec();
            var_r8 = 0;
            break;
        case 0x32:
            native_fn_0203ff14();
            var_r8 = 0;
            break;
        case 0x23:
            native_fn_0203e2dc();
            var_r8 = 0;
            break;
        case 0x24:
            native_fn_0203e464();
            var_r8 = 0;
            break;
        case 0x25:
            var_r8 = native_fn_0203e55c();
            break;
        case 0x27:
            native_fn_0203ffdc();
            var_r8 = 0;
            break;
        case 0x26:
            native_fn_0203d96c();
            var_r8 = 0;
            break;
        case 0x28:
            native_fn_0203f4b0();
            var_r8 = 0;
            break;
        case 0x2B:
            native_fn_0203f5b4();
            var_r8 = 0;
            break;
        case 0x2D:
            native_fn_0203f864();
            var_r8 = 0;
            break;
        case 0x2E:
            var_r8 = 0;
            break;
        case 0x2F:
            native_fn_0203f9a4();
            var_r8 = 0;
            break;
        case 0x30:
            var_r9 = native_fn_0203f1ec();
            var_r8 = 0;
            break;
        case 0x33:
            native_fn_0203f710();
            var_r8 = 1;
            break;
        }
    } while (var_r8 != 0);
    native_fn_02041764();
    return var_r9;
}
