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
#define NULL ((void *)0)
extern u32 native_fn_0202a634(void);
extern u32 native_fn_02041814(void);
extern u32 native_fn_020418b0(u32 value);
extern u32 native_fn_0207f254(void);
typedef u32 (*MenuCallback)(void);
extern MenuCallback native_data_020de4fc[];
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    u8 unknown_2[0xe];
    u32 field_10;
} Record_native_data_021c6c14;
extern Record_native_data_021c6c14 native_data_021c6c14;
u32 native_main_0207e874(void) {
    u32 var_r8;
    s32 var_r9;

    var_r8 = 0;
    native_fn_0202a634();
    do {
        var_r9 = 0;
        switch (native_data_021c6c14.field_10) {
        default:
            break;
        case 0:
            native_data_021c6c14.field_10 = 1U;
            var_r9 = 1;
            break;
        case 1:
            if (native_fn_02041814() != 1) {
                native_fn_020418b0(0);
                native_data_021c6c14.field_10 = 2U;
                var_r9 = 1;
            }
            break;
        case 2:
            if (native_data_020de4fc[native_data_021c6c14.field_1]() != 0) {
                native_data_021c6c14.field_10 = 3U;
                var_r9 = 1;
            }
            break;
        case 3:
            native_data_021c6c14.field_10 = 4U;
            var_r9 = 1;
            break;
        case 4:
            native_data_021c6c14.field_10 = 5U;
            var_r9 = 1;
            break;
        case 5:
            var_r8 = 1;
            break;
        }
    } while (var_r9 != 0);
    native_fn_0207f254();
    return var_r8;
}
