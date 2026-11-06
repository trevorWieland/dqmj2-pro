typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u8 unknown_00[0x4C];
    u32 field_4c;
    u8 unknown_50[0x48];
    u32 field_98;
} State;

typedef struct {
    u32 first;
    u32 second;
    u32 third;
} Triple;

extern State data_ov000_0223033c;
extern Triple data_ov000_02230398;
extern Triple data_ov000_022303b0;
extern const u8 data_ov000_0222b854[49];

u32 native_ov000_021d8528(u32 increment) {
    u32 counter;
    u32 result;
    counter = data_ov000_0223033c.field_98;
    result = data_ov000_0223033c.field_4c;
    data_ov000_0223033c.field_98 = counter + increment;
    return result;
}

void native_ov000_021d8abc(const Triple *source) {
    if (source != 0) {
        data_ov000_02230398 = *source;
        data_ov000_022303b0 = *source;
    }
}

s32 native_ov000_021da484(s32 index) {
    s8 values[49];
    s32 pairs;
    u8 *destination;
    const u8 *source;
    u8 second;
    u8 first;
    source = data_ov000_0222b854;
    destination = (u8 *)values;
    pairs = 24;
    do {
        first = source[0];
        second = source[1];
        source += 2;
        destination[0] = first;
        destination[1] = second;
        destination += 2;
        pairs--;
    } while (pairs != 0);
    *destination = *source;
    return values[index];
}

u32 native_ov000_021da434(u32 *value) {
    if (*value == 0) {
        return 0;
    }
    *value = 0;
    return 1;
}
