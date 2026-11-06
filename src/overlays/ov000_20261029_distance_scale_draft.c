typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
typedef signed long long s64;

typedef struct {
    unsigned int x;
    unsigned int y;
    unsigned int z;
} Ov000VectorWords;

typedef struct {
    u8 unknown_00[0xA4];
    u32 field_a4;
} State;

extern u32 func_ov000_021d8a44(void);
extern signed long long func_ov000_021d8c34(const Ov000VectorWords *input);
extern s64 runtime_main_02025f2c(s64 numerator, s64 denominator);

u8 native_ov000_021e035c(const Ov000VectorWords *input) {
    Ov000VectorWords local;
    const State *state;
    s64 distance;
    local = *input;
    state = (const State *)func_ov000_021d8a44();
    local.y += state->field_a4;
    distance = func_ov000_021d8c34(&local);
    if (distance < 0x400) {
        return 4;
    }
    if (distance >= 0x6400) {
        return 31;
    }
    return (u8)(runtime_main_02025f2c((distance - 0x400) * 22, 0x6000) + 4);
}
