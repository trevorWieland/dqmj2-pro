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

void native_ov002_021d7630(u32 value) {
    data_ov002_021da540[1] = value;
    func_0204b61c(data_ov002_021daec0[4], value);
    data_02101ae8[801] = 1;
}

void native_ov002_021d7668(u32 index, u32 value) {
    u32 narrowed = (u8)value;
    data_ov002_021da544[index] = narrowed;
    func_0204b138(data_ov002_021daec0[5], index, narrowed);
    data_02101ae8[801] = 1;
}

void native_ov002_021d76a8(u32 index, u32 first, u32 second) {
    func_02048a60(func_0205f98c(((u32 *)data_ov002_021daec0[5])[7], (u8)index), first, second);
    data_02101ae8[801] = 1;
}

void native_ov002_021d7744(u32 first, u32 second) {
    func_02048a60(data_ov002_021daec0[3], first, second);
    data_02101ae8[801] = 1;
}

void native_ov002_021d7810(void) {
    data_ov002_021daee4.value16 = 0;
    data_ov002_021daee4.value4 = 0;
    data_ov002_021daee4.a = 31;
    data_ov002_021daee4.b = 127;
    data_ov002_021daee4.c = 127;
    data_ov002_021daee4.value8 = 1;
}

void native_ov002_021d8504(u32 value) {
    data_ov002_021daee4.value8 = value;
}
