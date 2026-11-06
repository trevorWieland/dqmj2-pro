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

s32 native_ov002_021d7850(s32 value) {
    s8 index;
    s32 result = 0;
    s8 *entry;
    if (value == 127) {
        return 127;
    }
    entry = data_ov002_021da57b;
    index = 0;
    do {
        if (value == *entry) {
            result = index;
            break;
        }
        index++;
        entry += 3;
    } while (index < 21);
    return result;
}
