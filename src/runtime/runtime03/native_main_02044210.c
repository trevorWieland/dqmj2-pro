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
extern u32 native_fn_01ffa4b4();
extern u32 native_fn_020044ac();
extern u32 native_fn_020045d8();
extern u32 native_fn_0202a634();
extern u32 native_fn_02041764();
extern u32 native_fn_02043718();
extern u32 native_fn_0204379c();
extern u32 native_fn_020437d8();
extern u32 native_fn_02043844();
extern u32 native_fn_020438a4();
extern u32 native_fn_020439c4();
extern u32 native_fn_02043db0();
extern u32 native_fn_02043dd0();
extern u32 native_fn_02043e5c();
extern u32 native_fn_02043f90();
extern u32 native_fn_02043fb4();
extern u32 native_fn_02043fd8();
extern u32 native_fn_02044068();
extern u32 native_fn_02044088();
extern u32 native_fn_020440cc();
extern u32 native_fn_0204411c();
extern u32 native_fn_0204415c();
extern u32 native_fn_ov001_021f10c8();
extern u8 native_data_020f69c4[];
u32 native_main_02044210(void) {
    u32 var_r6;
    u32 var_r7;

    var_r6 = 1;
    var_r7 = 2;
    M2C_FIELD(native_data_020f69c4, u32 *, 0x10) = native_fn_0202a634();
    native_fn_020044ac();
    native_fn_020045d8();
    do {
        switch (M2C_FIELD(native_data_020f69c4, u8 *, 3)) {
        default:
            break;
        case 0:
            var_r6 = native_fn_02043718();
            break;
        case 1:
            var_r6 = native_fn_0204379c();
            break;
        case 2:
            var_r6 = native_fn_020437d8();
            break;
        case 3:
            var_r6 = native_fn_020438a4();
            break;
        case 4:
            var_r6 = native_fn_020439c4();
            break;
        case 5:
            var_r6 = native_fn_02043db0();
            break;
        case 6:
            var_r6 = native_fn_02043dd0();
            break;
        case 7:
            var_r6 = native_fn_02043e5c();
            break;
        case 8:
            var_r6 = native_fn_02043f90();
            break;
        case 9:
            var_r6 = native_fn_02043fb4();
            break;
        case 10:
            var_r6 = native_fn_02043fd8();
            break;
        case 11:
            var_r6 = native_fn_02044068();
            break;
        case 12:
            var_r6 = native_fn_02044088();
            break;
        case 13:
            var_r6 = native_fn_020440cc();
            break;
        case 15:
            var_r6 = native_fn_0204411c();
            break;
        case 16:
            var_r6 = native_fn_02043844();
            break;
        case 17:
            var_r7 = native_fn_0204415c();
            var_r6 = 0;
            break;
        }
    } while (var_r6 != 0);
    native_fn_ov001_021f10c8();
    native_fn_01ffa4b4();
    native_fn_02041764();
    return var_r7;
}
