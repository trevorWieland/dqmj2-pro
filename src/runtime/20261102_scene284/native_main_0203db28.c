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
extern u32 native_fn_0202ac08(u32);
extern u32 native_fn_0203d310(void);
extern u32 native_fn_0203d324(void);
extern u32 native_fn_0203d338(void);
extern u32 native_fn_020407fc(void);
extern u8 native_fn_0205bfd4(void);
extern u32 native_fn_02066c64(u32);
extern u32 native_fn_02066e98(void);
extern s32 native_fn_020c55dc(void);
extern u32 native_fn_020c56f8(void);
extern u32 native_fn_ov000_021d8c80(u32);
extern u32 native_fn_ov000_021d900c(u32);
extern u32 native_fn_ov000_021d9088(void);
extern u32 native_fn_ov000_021d92b4(u32);
extern u32 native_fn_ov000_021d9580(u8);
extern u32 native_fn_ov000_021d966c(u32);
extern u32 native_fn_ov000_021d99ac(u32);
extern u32 native_fn_ov000_021da454(u32);
extern u32 native_fn_ov000_021dd4bc(u32);
extern u32 native_fn_ov000_021dea48(u32);
extern u32 native_fn_ov000_021df200(u32);
extern u32 native_fn_ov000_021df3f4(void);
extern u32 native_fn_ov000_021df4ec(void);
extern u32 native_fn_ov000_021e0944(u32);
extern u32 native_fn_ov000_021e33d8(void);
extern u32 native_fn_ov000_021e4014(u32);
extern u32 native_fn_ov000_021e4d04(u32);
extern u32 native_fn_ov000_021e4e9c(u32);
extern u32 native_fn_ov000_021e725c(void);
extern u32 native_fn_ov000_021e7aec(void);
extern u32 native_fn_ov000_021e7bd4(void);
extern u32 native_fn_ov000_02209c04(void);
extern u32 native_fn_ov000_02211098(void);
extern u32 native_fn_ov000_022127a8(void);
extern u32 native_fn_ov000_02212b20(void);
typedef struct {
    u8 unknown_0[0x4];
    s8 field_4;
    u8 unknown_5[0x5];
    s8 field_a;
    u8 unknown_b[0x1];
    u8 field_c;
} Record_native_data_020f6054;
extern Record_native_data_020f6054 native_data_020f6054;
extern u8 native_data_020f60a8[];
u32 native_main_0203db28(void) {
    u32 var_r0;

    native_fn_ov000_02211098();
    native_fn_ov000_021e33d8();
    native_fn_ov000_021e7aec();
    native_fn_ov000_021df4ec();
    native_fn_ov000_021df3f4();
    native_fn_0202ac08((u32) native_data_020f60a8);
    native_fn_0203d310();
    native_fn_0203d324();
    native_fn_0203d338();
    native_fn_ov000_021df200(native_data_020f6054.field_c);
    if (native_fn_020407fc() == 0) {
        native_fn_ov000_021e725c();
        native_fn_ov000_02212b20();
        native_fn_ov000_021d900c(0xFF);
        native_fn_ov000_021d92b4(0xFF);
        native_fn_ov000_021d9580(0xFF);
        native_fn_ov000_021e4014(0xFF);
        native_fn_ov000_021d9088();
        native_fn_ov000_021da454(0xFF);
        native_fn_ov000_021dd4bc(0xFF);
        native_fn_ov000_021d966c(0xFF);
        native_fn_ov000_021dea48(0xFF);
        if (native_fn_0205bfd4() != 0) {
            var_r0 = 2;
        } else {
            var_r0 = 0;
        }
        native_fn_ov000_021d99ac(var_r0);
    }
    native_fn_ov000_021e4d04(0xFF);
    if (native_fn_020407fc() == 0) {
        native_fn_020c55dc();
        native_fn_02066e98();
        native_fn_02066c64(0xFF);
        native_fn_ov000_021e7bd4();
        native_fn_ov000_02209c04();
        native_fn_ov000_022127a8();
        native_fn_020c56f8();
    }
    native_fn_ov000_021d8c80(1);
    native_fn_ov000_021e0944(native_data_020f6054.field_4);
    if (native_fn_ov000_021e4e9c(0x80) != 0) {
        native_data_020f6054.field_a = 0x31;
    } else {
        native_data_020f6054.field_a = 2;
    }
    return 1U;
}
