typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;

typedef struct {
    u32 x;
    u32 y;
    u32 z;
} Vector;

typedef struct {
    u8 unknown_00[0x5C];
    Vector vector;
} State;

extern State data_ov000_0223033c;

s64 native_ov000_021d8c34(const Vector *input) {
    s32 dy;
    s32 dx;
    s32 dz;
    u64 sum;
    dx = (s32)(data_ov000_0223033c.vector.x - input->x);
    sum = (s64)dx * dx;
    dy = (s32)(data_ov000_0223033c.vector.y - input->y);
    sum += (s64)dy * dy;
    dz = (s32)(data_ov000_0223033c.vector.z - input->z);
    sum += (s64)dz * dz;
    return (s64)sum >> 12;
}
