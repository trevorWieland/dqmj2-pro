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
typedef struct {u16 first;u16 second;} Pair;
extern u32 native_fn_02044424();
extern const u8 *native_fn_0207afec(u32);
void native_ov001_021e8d28(u8 *destination, void *enemy) {
    const u8 *table;
    u32 enabled;
    u8 suppressed;
    s32 sourceIndex;
    u8 *fields;
    const Pair *pairs;
    s32 targetIndex;

    fields = destination + 0xC;
    pairs = (const void *)((u8 *)enemy + 4);
    sourceIndex = 0;
    do {
        *(fields + sourceIndex) = (s8) pairs[sourceIndex].second;
        sourceIndex += 1;
    } while (sourceIndex < 6);
    enabled = native_fn_02044424(8);
    if (enabled == 0) {
        return;
    }
    suppressed = M2C_FIELD(enemy, u8 *, 0x63);
    if (suppressed != 0) {
        return;
    }
    table = native_fn_0207afec(0);
    targetIndex = 0;
    do {
        *(fields + targetIndex) = M2C_FIELD(((*(fields + targetIndex) * 0x28) + table), u8 *, 0x23);
        targetIndex += 1;
    } while (targetIndex < 6);
    return;
}
