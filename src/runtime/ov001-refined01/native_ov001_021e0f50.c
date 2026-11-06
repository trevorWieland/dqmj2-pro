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
extern u32 native_fn_0202a634();
extern u32 native_fn_0204437c();
extern u32 native_fn_0204439c();
extern u32 native_fn_ov001_021ddc00();
extern u32 native_fn_ov001_021ddc6c();
extern u32 native_fn_ov001_021ddd44();
extern u32 native_fn_ov001_021ddd80();
extern u32 native_fn_ov001_021ddf34();
extern u32 native_fn_ov001_021de254();
extern u32 native_fn_ov001_021de40c();
extern u32 native_fn_ov001_021de598();
extern u32 native_fn_ov001_021de644();
extern u32 native_fn_ov001_021de984();
extern u32 native_fn_ov001_021dee18();
extern u32 native_fn_ov001_021df310();
extern u32 native_fn_ov001_021df364();
extern u32 native_fn_ov001_021df388();
extern u32 native_fn_ov001_021df3ac();
extern u32 native_fn_ov001_021df3d0();
extern u32 native_fn_ov001_021df3f0();
extern u32 native_fn_ov001_021df414();
extern u32 native_fn_ov001_021df42c();
extern u32 native_fn_ov001_021df450();
extern u32 native_fn_ov001_021df470();
extern u32 native_fn_ov001_021df494();
extern u32 native_fn_ov001_021df4b4();
extern u32 native_fn_ov001_021df558();
extern u32 native_fn_ov001_021df640();
extern u32 native_fn_ov001_021df680();
extern u32 native_fn_ov001_021df808();
extern u32 native_fn_ov001_021df8d0();
extern u32 native_fn_ov001_021df9a8();
extern u32 native_fn_ov001_021df9e4();
extern u32 native_fn_ov001_021dfa34();
extern u32 native_fn_ov001_021dfa64();
extern u32 native_fn_ov001_021dfa84();
extern u32 native_fn_ov001_021dfac4();
extern u32 native_fn_ov001_021dfae4();
extern u32 native_fn_ov001_021dfd74();
extern u32 native_fn_ov001_021dff00();
extern u32 native_fn_ov001_021e00b4();
extern u32 native_fn_ov001_021e0328();
extern u32 native_fn_ov001_021e05d4();
extern u32 native_fn_ov001_021e0724();
extern u32 native_fn_ov001_021e07f0();
extern u32 native_fn_ov001_021e081c();
extern u32 native_fn_ov001_021e08bc();
extern u32 native_fn_ov001_021e08e4();
extern u32 native_fn_ov001_021e0c70();
extern u32 native_fn_ov001_021e0c94();
extern u32 native_fn_ov001_021e0cb8();
extern u32 native_fn_ov001_021e0d44();
extern u32 native_fn_ov001_021e0d64();
extern u32 native_fn_ov001_021e0d88();
extern u32 native_fn_ov001_021e0f38();
extern u32 native_fn_ov001_021e0f40();
extern u32 native_fn_ov001_021e0f48();
extern u32 native_fn_ov001_02210cd4();
typedef struct {
    u8 unknown_0[0x8];
    u8 field_8;
    u8 unknown_9[0x43];
    u32 field_4c;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021e0f50(void) {
    u32 var_r7;
    s32 var_r8;
    u32 var_r9;

    var_r7 = 1;
    var_r8 = 1;
    var_r9 = 0;
    native_data_ov001_022388ec.field_4c = native_fn_0202a634();
    do {
        switch (native_data_ov001_022388ec.field_8) {
        default:
            break;
        case 0x0:
            var_r7 = native_fn_ov001_021ddc00();
            break;
        case 0x1:
            var_r7 = native_fn_ov001_021ddc6c();
            break;
        case 0x2:
            var_r7 = native_fn_ov001_021de40c();
            break;
        case 0x24:
            var_r7 = native_fn_ov001_021ddd44();
            break;
        case 0x25:
            var_r7 = native_fn_ov001_021ddd80();
            break;
        case 0x26:
            var_r7 = native_fn_ov001_021ddf34();
            break;
        case 0x27:
            var_r7 = native_fn_ov001_021de254();
            break;
        case 0x3:
            var_r7 = native_fn_ov001_021de598();
            break;
        case 0x4:
            var_r7 = native_fn_ov001_021dee18();
            break;
        case 0x5:
            var_r7 = native_fn_ov001_021df310();
            break;
        case 0x6:
            var_r7 = native_fn_ov001_021df364();
            break;
        case 0x7:
            var_r7 = native_fn_ov001_021df388();
            break;
        case 0x8:
            var_r7 = native_fn_ov001_021df3ac();
            break;
        case 0x9:
            var_r7 = native_fn_ov001_021df3d0();
            break;
        case 0xA:
            var_r7 = native_fn_ov001_021df3f0();
            break;
        case 0xB:
            var_r7 = native_fn_ov001_021df414();
            break;
        case 0xC:
            var_r7 = native_fn_ov001_021df42c();
            break;
        case 0xD:
            var_r7 = native_fn_ov001_021df450();
            break;
        case 0xE:
            var_r7 = native_fn_ov001_021df470();
            break;
        case 0x11:
            var_r7 = native_fn_ov001_021df494();
            break;
        case 0x12:
            var_r7 = native_fn_ov001_021df4b4();
            break;
        case 0x13:
            var_r7 = native_fn_ov001_021df9a8();
            break;
        case 0x14:
            var_r7 = native_fn_ov001_021df9e4();
            break;
        case 0x15:
            var_r7 = native_fn_ov001_021dfa34();
            break;
        case 0x16:
            var_r7 = native_fn_ov001_021dfa64();
            break;
        case 0x17:
            var_r7 = native_fn_ov001_021dfa84();
            break;
        case 0x34:
            var_r7 = native_fn_ov001_021e0d44();
            break;
        case 0x35:
            var_r7 = native_fn_ov001_021e0d64();
            break;
        case 0x28:
            var_r7 = native_fn_ov001_021dfac4();
            break;
        case 0x29:
            var_r7 = native_fn_ov001_021dfae4();
            break;
        case 0x2C:
            var_r7 = native_fn_ov001_021df680();
            break;
        case 0x2D:
            var_r7 = native_fn_ov001_021df808();
            break;
        case 0xF:
            var_r7 = native_fn_ov001_021df558();
            break;
        case 0x10:
            var_r7 = native_fn_ov001_021df640();
            break;
        case 0x18:
            var_r7 = native_fn_ov001_021df8d0();
            break;
        case 0x19:
            var_r7 = native_fn_ov001_021dfd74();
            break;
        case 0x1A:
            var_r7 = native_fn_ov001_021dff00();
            break;
        case 0x1B:
            var_r7 = native_fn_ov001_021e00b4();
            break;
        case 0x1C:
            var_r7 = native_fn_ov001_021e0328();
            break;
        case 0x1D:
            var_r7 = native_fn_ov001_021e05d4();
            break;
        case 0x1E:
            var_r7 = native_fn_ov001_021e0724();
            break;
        case 0x1F:
            var_r7 = native_fn_ov001_021e07f0();
            break;
        case 0x20:
            var_r7 = native_fn_ov001_021e081c();
            break;
        case 0x21:
            var_r7 = native_fn_ov001_021de644();
            break;
        case 0x22:
            var_r7 = native_fn_ov001_021de984();
            break;
        case 0x2A:
            var_r7 = native_fn_ov001_021e08bc();
            break;
        case 0x2B:
            var_r7 = native_fn_ov001_021e08e4();
            break;
        case 0x23:
            var_r7 = native_fn_ov001_021e0c70();
            break;
        case 0x32:
            var_r7 = native_fn_ov001_021e0c94();
            break;
        case 0x33:
            var_r7 = native_fn_ov001_021e0cb8();
            break;
        case 0x2E:
            var_r7 = native_fn_ov001_021e0f38();
            var_r8 = 0;
            break;
        case 0x2F:
            var_r7 = native_fn_ov001_021e0f40();
            var_r8 = 0;
            break;
        case 0x30:
            var_r7 = native_fn_ov001_021e0f48();
            var_r8 = 0;
            break;
        case 0x31:
        case 0x36:
            native_fn_ov001_021e0d88();
            var_r7 = 0;
            var_r8 = 0;
            var_r9 = 1;
            break;
        }
    } while (var_r7 != 0);
    if (var_r8 != 0) {
        native_fn_ov001_02210cd4();
        native_fn_0204437c();
        native_fn_0204439c();
    }
    return var_r9;
}
