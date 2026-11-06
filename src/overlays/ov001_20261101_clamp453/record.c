#include "context.h"
void native_ov001_021e46d8(u8 *record, s16 *delta) {
    s32 kind, tag, left, leftTag, right, rightTag;
    s32 maximum, current;
    kind = M2C_FIELD(record, s16 *, 0x18);
    tag = M2C_FIELD(record, u8 *, 0x1a);
    left = M2C_FIELD(record, s16 *, 0x40);
    leftTag = M2C_FIELD(record, u8 *, 0x4c);
    right = M2C_FIELD(record, s16 *, 0x42);
    rightTag = M2C_FIELD(record, u8 *, 0x4d);
    maximum = native_fn_ov001_021e8e34(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(record, s16 *, 0x20);
    if (current > maximum) {
        delta[0] -= current - maximum;
        M2C_FIELD(record, s16 *, 0x20) = maximum;
    }
    maximum = native_fn_ov001_021e8ebc(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(record, s16 *, 0x22);
    if (current > maximum) {
        delta[1] -= current - maximum;
        M2C_FIELD(record, s16 *, 0x22) = maximum;
    }
    maximum = native_fn_ov001_021e8f44(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(record, s16 *, 0x28);
    if (current > maximum) {
        delta[2] -= current - maximum;
        M2C_FIELD(record, s16 *, 0x28) = maximum;
    }
    maximum = native_fn_ov001_021e8fcc(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(record, s16 *, 0x2a);
    if (current > maximum) {
        delta[3] -= current - maximum;
        M2C_FIELD(record, s16 *, 0x2a) = maximum;
    }
    maximum = native_fn_ov001_021e9054(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(record, s16 *, 0x2c);
    if (current > maximum) {
        delta[4] -= current - maximum;
        M2C_FIELD(record, s16 *, 0x2c) = maximum;
    }
    maximum = native_fn_ov001_021e90dc(kind, tag, left, leftTag, right, rightTag);
    current = M2C_FIELD(record, s16 *, 0x2e);
    if (current > maximum) {
        delta[5] -= current - maximum;
        M2C_FIELD(record, s16 *, 0x2e) = maximum;
    }
}
