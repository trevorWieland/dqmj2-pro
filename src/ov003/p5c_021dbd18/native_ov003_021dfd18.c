typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u8 native_data_02101ae8[];
extern u8 native_data_ov003_021e041c[];
extern u8 native_data_ov003_021e0d18[];

extern void native_fn_0204b61c(u32, s32);

#define FIELD(base, type, offset) (*(type *)((u8 *)(base) + (offset)))

void native_ov003_021dfd18(s32 value) {
    u32 *context = (u32 *)native_data_ov003_021e0d18;

    native_data_ov003_021e041c[1] = value;
    native_fn_0204b61c(context[4], value);
    FIELD(native_data_02101ae8, u32, 0xc84) = 1;
}
