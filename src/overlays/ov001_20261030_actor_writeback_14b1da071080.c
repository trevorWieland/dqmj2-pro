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
extern u32 native_fn_02008e0c();
extern u32 native_fn_0205d7cc();
extern u32 native_fn_ov001_021d8dec();
extern u32 native_fn_ov001_021d9d0c();
typedef struct {u32 words[8];} StatBlock;
u32 native_ov001_021da268(void *records, void *actors, s32 restoreCurrent) {
    s32 preserveStatus;
    u8 secondByte;
    u8 firstByte;
    s32 pairsRemaining;
    u8 actorPresent;
    void *copyTarget;
    void *copySource;
    s32 slot;
    s32 statusIndex;
    u32 processed;
    void *actor;
    void *record;

    processed = 0;
    record = records;
    actor = actors;
    slot = 0;
    do {
        if ((s32) M2C_FIELD(record, s16 *, 0x2E) >= 0) {
            if (restoreCurrent != 0) {
                native_fn_ov001_021d9d0c(actor);
            }
            *(StatBlock *)(record + 0x11C) = *(const StatBlock *)(actor + 0x1EC);
            copySource = actor + 0x22C;
            copyTarget = record + 0x13C;
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
            native_fn_02008e0c(actor + 0x432, record + 0x203, 0xA);
            statusIndex = 0;
            M2C_FIELD(record, u8 *, 0x20D) = (u8) M2C_FIELD(actor, u8 *, 0x43C);
            do {
                if (native_fn_0205d7cc(M2C_FIELD((void *) native_fn_ov001_021d8dec(statusIndex), s16 *, 4)) & 1) {
                    preserveStatus = 1;
                } else {
                    preserveStatus = 0;
                }
                if (preserveStatus == 0) {
                    M2C_FIELD((record + statusIndex), s8 *, 0x1C4) = (s8) M2C_FIELD((actor + statusIndex), s8 *, 0x39E);
                }
                statusIndex += 1;
            } while (statusIndex < 0x3C);
            native_fn_02008e0c(actor + 0x21C, record + 0x1B4, 0x10);
            M2C_FIELD(record, s8 *, 0x202) = 1;
            actorPresent = M2C_FIELD(actor, u8 *, 0x31C);
            if ((actorPresent != 0) && (M2C_FIELD(actor, u8 *, 0x1FF) != 0)) {
                M2C_FIELD(record, s8 *, 0x201) = 1;
            } else if ((actorPresent != 0) && (M2C_FIELD(M2C_FIELD(actor, void **, 0x1E8), u8 *, 0xAC) != 0)) {
                M2C_FIELD(record, s8 *, 0x201) = 2;
            } else {
                M2C_FIELD(record, s8 *, 0x201) = 0;
            }
            processed += 1;
        } else {
            M2C_FIELD(record, s8 *, 0x201) = 3;
        }
        slot += 1;
        record += 0x210;
        actor += 0x440;
    } while (slot < 3);
    return processed;
}
