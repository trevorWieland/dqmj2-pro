#define NULL ((void *)0)
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
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_utility_child_arm9_arm_02009e90();
extern u32 native_utility_child_arm9_thumb_0200b08c();
extern u32 native_utility_child_arm9_thumb_0200b07c();
u32 native_utility_child_arm9_main_0200b8e8(void *arg0) {
    void *var_r0;
    void *temp_r6;

    native_utility_child_arm9_thumb_0200b08c();
    var_r0 = CHILD_FIELD(arg0, void **, 0x18);
    if (var_r0 != NULL) {
        do {
            temp_r6 = CHILD_FIELD(var_r0, void **, 4);
            CHILD_FIELD(var_r0, s32 *, 0) = 0;
            CHILD_FIELD(var_r0, void **, 4) = NULL;
            native_utility_child_arm9_arm_02009e90(var_r0, 8);
            var_r0 = temp_r6;
        } while (temp_r6 != NULL);
    }
    return native_utility_child_arm9_thumb_0200b07c();
}
