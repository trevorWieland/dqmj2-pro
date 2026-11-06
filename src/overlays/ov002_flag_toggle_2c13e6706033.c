typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef int s32;

extern u32 data_ov002_021daec0[];
extern u8 data_ov002_021da540[];
extern u8 data_ov002_021da544[];
extern u32 data_02101ae8[];
extern s8 data_ov002_021da57b[];

typedef struct {
    u8 a;
    u8 b;
    u8 c;
    u8 d;
    u32 value4;
    u32 value8;
    u32 value12;
    u32 value16;
} State;

extern State data_ov002_021daee4;
extern void func_0204b61c(u32, u32);
extern void func_0204b138(u32, u32, u32);
extern u32 func_0205f98c(u32, u32);
extern void func_02048a60(u32, u32, u32);

void native_ov002_021d76f0(u32 flag) {
    data_ov002_021da540[0] = flag;
    if (flag != 0) {
        ((u32 *)data_ov002_021daec0[3])[31] = ((u32 *)data_ov002_021daec0[3])[31] | 2;
    } else {
        ((u32 *)data_ov002_021daec0[3])[31] = ((u32 *)data_ov002_021daec0[3])[31] & ~2;
    }
    data_02101ae8[801] = 1;
}
