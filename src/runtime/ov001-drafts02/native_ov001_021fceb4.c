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
extern u32 native_fn_02048f7c();
extern u32 native_fn_0206c87c();
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021dc568();
extern u32 native_fn_ov001_021fc9a4();
extern u32 native_fn_ov001_02204944();
extern u32 native_fn_ov001_02204c84();
typedef struct {
    u8 unknown_0[0x3];
    s8 field_3;
} Record_native_data_ov001_0222ed34;
extern Record_native_data_ov001_0222ed34 native_data_ov001_0222ed34;
void native_ov001_021fceb4(void) {
    u32 temp_r5;
    s8 var_r7;
    s8 var_r8;

    native_fn_0206c87c(0);
    native_fn_ov001_021fc9a4(0);
    native_fn_ov001_021fc9a4(1);
    var_r8 = 0;
    do {
        var_r7 = 0;
loop_2:
        temp_r5 = native_fn_ov001_021db438(var_r8, var_r7);
        native_fn_ov001_02204944(var_r8, var_r7, 1);
        native_fn_ov001_021dc568(temp_r5);
        var_r7 += 1;
        if ((s32) var_r7 < 3) {
            goto loop_2;
        }
        var_r8 += 1;
    } while ((s32) var_r8 < 2);
    native_data_ov001_0222ed34.field_3 = (s8) native_fn_ov001_02204c84(0xE0, 0x60, native_fn_02048f7c(1));
}
