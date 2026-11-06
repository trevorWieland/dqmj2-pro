typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u32 x;
    u32 y;
    u32 z;
} Vector;

typedef struct {
    u8 unknown_00[0x54];
    u32 field_54;
    u32 field_58;
    u8 unknown_5c[0x40];
    u32 field_9c;
    u32 field_a0;
    u32 field_a4;
} State;

extern const Vector data_ov000_0222b7f0[];
extern State data_ov000_0223033c;

void native_ov000_021d8c80(s32 index) {
    u32 x;
    u32 y;
    u32 z;
    x = data_ov000_0222b7f0[index].x;
    y = data_ov000_0222b7f0[index].y;
    z = data_ov000_0222b7f0[index].z;
    data_ov000_0223033c.field_a0 = x;
    data_ov000_0223033c.field_9c = y;
    data_ov000_0223033c.field_a4 = z;
    data_ov000_0223033c.field_54 = x;
    data_ov000_0223033c.field_58 = z;
}
