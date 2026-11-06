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
typedef struct {u32 words[8];} StatBlock;
void native_ov001_021d9e9c(void *actor, void *record) {
    s16 var_r1;
    s16 var_r1_2;
    s16 var_r1_3;
    s16 var_r1_4;
    s16 var_r1_5;
    s16 var_r1_6;
    s16 var_r1_7;

    *(StatBlock *)(actor + 0x1EC) = *(const StatBlock *)(record + 0x11C);
    var_r1 = (s16) M2C_FIELD(actor, s16 *, 0x1EC);
    if ((s32) var_r1 >= 0x270F) {
        var_r1 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1EC) = var_r1;
    var_r1_2 = M2C_FIELD(actor, s16 *, 0x1EE);
    if ((s32) var_r1_2 >= 0x270F) {
        var_r1_2 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1EE) = var_r1_2;
    var_r1_3 = M2C_FIELD(actor, s16 *, 0x1F0);
    if ((s32) var_r1_3 >= 0x270F) {
        var_r1_3 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1F0) = var_r1_3;
    var_r1_4 = M2C_FIELD(actor, s16 *, 0x1F4);
    if ((s32) var_r1_4 >= 0x270F) {
        var_r1_4 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1F4) = var_r1_4;
    var_r1_5 = M2C_FIELD(actor, s16 *, 0x1F6);
    if ((s32) var_r1_5 >= 0x270F) {
        var_r1_5 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1F6) = var_r1_5;
    var_r1_6 = M2C_FIELD(actor, s16 *, 0x1F8);
    if ((s32) var_r1_6 >= 0x270F) {
        var_r1_6 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1F8) = var_r1_6;
    var_r1_7 = M2C_FIELD(actor, s16 *, 0x1FA);
    if ((s32) var_r1_7 >= 0x270F) {
        var_r1_7 = 0x270F;
    }
    M2C_FIELD(actor, s16 *, 0x1FA) = var_r1_7;
    return;
}
