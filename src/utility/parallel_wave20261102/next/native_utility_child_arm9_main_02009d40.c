typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

void native_utility_child_arm9_main_02009d40(void *arg0, void *arg1) {
    void *temp_r3;

    temp_r3 = CHILD_FIELD(arg0, void **, 0x8C);
    if (temp_r3 == 0) {
        CHILD_FIELD(arg0, void **, 0x88) = arg1;
    } else {
        CHILD_FIELD(temp_r3, void **, 0x10) = arg1;
    }
    CHILD_FIELD(arg1, void **, 0x14) = temp_r3;
    CHILD_FIELD(arg1, s32 *, 0x10) = 0;
    CHILD_FIELD(arg0, void **, 0x8C) = arg1;
}
