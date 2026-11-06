#include "context.h"
void native_ov001_021e4500(u8 *actor, s16 *delta) {
    s32 kind, tag, left, leftTag, right, rightTag;
    u8 *descriptor, *record;
    s32 maximum, current;
    descriptor = M2C_FIELD(actor, u8 **, 0x1E8);
    kind = M2C_FIELD(descriptor, s16 *, 0x2A);
    tag = M2C_FIELD(descriptor, u8 *, 0x2C);
    record = native_fn_02062a10(M2C_FIELD(descriptor, u32 *, 0));
    left = M2C_FIELD(record, s16 *, 0x40);
    leftTag = M2C_FIELD(record, u8 *, 0x4C);
    right = M2C_FIELD(record, s16 *, 0x42);
    rightTag = M2C_FIELD(record, u8 *, 0x4D);
    maximum = native_fn_ov001_021e8e34(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(actor, s16 *, 0x1ec);
    if (current > maximum) {
        delta[0] -= current - maximum;
        M2C_FIELD(actor, s16 *, 0x1ec) = maximum;
    }
    maximum = native_fn_ov001_021e8ebc(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(actor, s16 *, 0x1ee);
    if (current > maximum) {
        delta[1] -= current - maximum;
        M2C_FIELD(actor, s16 *, 0x1ee) = maximum;
    }
    maximum = native_fn_ov001_021e8f44(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(actor, s16 *, 0x1f4);
    if (current > maximum) {
        delta[2] -= current - maximum;
        M2C_FIELD(actor, s16 *, 0x1f4) = maximum;
    }
    maximum = native_fn_ov001_021e8fcc(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(actor, s16 *, 0x1f6);
    if (current > maximum) {
        delta[3] -= current - maximum;
        M2C_FIELD(actor, s16 *, 0x1f6) = maximum;
    }
    maximum = native_fn_ov001_021e9054(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(actor, s16 *, 0x1f8);
    if (current > maximum) {
        delta[4] -= current - maximum;
        M2C_FIELD(actor, s16 *, 0x1f8) = maximum;
    }
    maximum = native_fn_ov001_021e90dc(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(actor, s16 *, 0x1fa);
    if (current > maximum) {
        delta[5] -= current - maximum;
        M2C_FIELD(actor, s16 *, 0x1fa) = maximum;
    }
    current = M2C_FIELD(actor, s16 *, 0x208);
    if (current > 9999) {
        delta[7] -= current - 9999;
        M2C_FIELD(actor, s16 *, 0x208) = 9999;
    }
}
