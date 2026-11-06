typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
u8 native_data_021c4f60[0x70];
static u32 service_calls;
static u32 failures;
u32 page_count_reset(u32 previous) {
    u32 index;
    for (index = 0; index < 0x70; index++) native_data_021c4f60[index] = 0xA5;
    native_data_021c4f60[0x61] = (u8)previous;
    service_calls = 0;
    failures = 0;
    return 0;
}
u32 page_count_status(void) {
    return failures | (service_calls << 16);
}
u32 native_fn_0206e2fc(u32 a, u32 b, u32 c, u32 d, u32 e) {
    u32 index = service_calls++;
    if (index > 1 || a != index || b != (index ? 31U : 0U) || c != 21 || d != index || e != 0) failures |= 1;
    return 0xCAFE0000U + index;
}
u32 native_fn_0206e388(s8 a, s8 b) {
    if (service_calls != 2 || a != 4 || b != 5) failures |= 2;
    service_calls++;
    return 0xBAD0BAD0U;
}
