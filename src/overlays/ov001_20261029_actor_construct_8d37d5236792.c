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
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern u32 native_fn_020649ac(u32);
extern u32 native_fn_020649c0(u32);
extern u32 native_fn_020649d4(u32);
extern u32 native_fn_020649e8(u32);
extern u32 native_fn_ov001_021d9960();
extern u32 native_fn_ov001_021d9a04();
extern u32 native_fn_ov001_021d9e20();
extern u32 native_fn_ov001_021d9e9c();
extern u8 native_data_ov001_022355ec[];
extern u8 native_data_ov001_022362ac[];
extern u8 native_data_ov001_02236f6c[];
extern u8 native_data_ov001_02237c2c[];
u32 native_ov001_021d9f70(s32 team) {
    u8 secondByte;
    u8 rank;
    s32 actionId;
    u8 firstByte;
    s32 pairsRemaining;
    u8 *copyTarget;
    s32 slot;
    u32 present;
    u32 record;
    u8 *actor;
    void *copySource;

    if (team == 0) {
        actor = native_data_ov001_02236f6c;
        record = native_fn_020649ac(0);
    } else if (team == 1) {
        actor = native_data_ov001_022362ac;
        record = native_fn_020649c0(0);
    } else if (team == 2) {
        actor = native_data_ov001_022355ec;
        record = native_fn_020649d4(0);
    } else {
        actor = native_data_ov001_02237c2c;
        record = native_fn_020649e8(0);
    }
    native_fn_02008d78(actor, 0, 0xCC0);
    present = 0;
    slot = 0;
    do {
        if ((s32) M2C_FIELD(record, s16 *, 0x2E) > 0) {
            M2C_FIELD(actor, s8 *, 0x31E) = team;
            M2C_FIELD(actor, s8 *, 0x31F) = slot;
            M2C_FIELD(actor, u8 *, 0x322) = (u8) native_fn_ov001_021d9960(team, M2C_FIELD(record, u8 *, 0xAD));
            M2C_FIELD(actor, s32 *, 0x1E8) = (s32) (record + 4);
            copySource = record + 0x13C;
            copyTarget = actor + 0x22C;
            pairsRemaining = 0x3C;
            do {
                firstByte = M2C_FIELD(copySource, u8 *, 0);
                secondByte = M2C_FIELD(copySource, u8 *, 1);
                copySource += 2;
                pairsRemaining -= 1;
                M2C_FIELD(copyTarget, u8 *, 0) = firstByte;
                M2C_FIELD(copyTarget, u8 *, 1) = secondByte;
                copyTarget += 2;
            } while (pairsRemaining != 0);
            native_fn_02008e0c(record + 0x1C4, actor + 0x39E, 0x3C);
            native_fn_02008e0c(record + 0x203, actor + 0x432, 0xA);
            M2C_FIELD(actor, u8 *, 0x43C) = (u8) M2C_FIELD(record, u8 *, 0x20D);
            native_fn_ov001_021d9e9c(actor, (void *) record);
            rank = M2C_FIELD(actor, u8 *, 0x322);
            if ((rank != 0) && (rank != 3)) {

            } else {
                actionId = 0;
                do {
                    if (M2C_FIELD((record + ((actionId >> 5) * 4)), s32 *, 0xC) & (1U << (actionId & 0x1F))) {
                        M2C_FIELD(&actor[M2C_FIELD(actor, u8 *, 0x323)], s8 *, 0x35E) = actionId;
                        M2C_FIELD(actor, u8 *, 0x323) = (u8) (M2C_FIELD(actor, u8 *, 0x323) + 1);
                    }
                    actionId += 1;
                } while ((s32) actionId < 0x100);
                native_fn_ov001_021d9e20(actor + 0x35E, M2C_FIELD(actor, u8 *, 0x323));
            }
            native_fn_ov001_021d9a04((void *) record, actor);
            M2C_FIELD(actor, s8 *, 0x31C) = 1;
            present += 1;
        }
        slot += 1;
        record += 0x210;
        actor += 0x440;
    } while ((s32) slot < 3);
    return present;
}
