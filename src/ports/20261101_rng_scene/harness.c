typedef unsigned char u8;
typedef unsigned int u32;
__declspec(align(4)) u8 native_data_020f6044[4];
__declspec(align(4)) u8 native_data_020f69c4[64];
static u32 current_case;
static u32 call_count;
static u32 call_ids[8];
static u32 call_args[8];
extern u32 native_main_02043844(void);
static u32 service(u32 id, u32 arg) {
    call_ids[call_count] = id;
    call_args[call_count++] = arg;
    return 0xA5438440U ^ current_case ^ id;
}
u32 native_fn_ov001_021d9710(void) {
    return service(0x021D9710U, 0);
}
u32 native_fn_ov001_021f92d8(void) {
    return service(0x021F92D8U, 0);
}
u32 native_fn_ov001_0220b48c(void) {
    return service(0x0220B48CU, 0);
}
u32 native_fn_ov001_0220b634(void) {
    return service(0x0220B634U, 0);
}
u32 native_fn_ov001_0220b3bc(void) {
    return service(0x0220B3BCU, 0);
}
void native_fn_ov001_022139e8(u32 value) {
    service(0x022139E8U, value);
}
u32 native_fn_ov001_0220268c(u32 value) {
    return service(0x0220268CU, value);
}
u32 native_fn_ov001_0220345c(u32 value) {
    return service(0x0220345CU, value);
}
__declspec(dllexport) void j2p_prepare(const u8 *frame, u32 seed, u32 index) {
    u32 i;
    for (i = 0; i < 64; ++i) native_data_020f69c4[i] = frame[i];
    for (i = 0; i < 4; ++i) native_data_020f6044[i] = (u8)(seed >> (i * 8));
    current_case = index;
    call_count = 0;
}
__declspec(dllexport) u32 j2p_run(void) {
    return native_main_02043844();
}
__declspec(dllexport) void j2p_state(u8 *frame, u8 *seed, u32 *ids, u32 *args, u32 *count) {
    u32 i;
    for (i = 0; i < 64; ++i) frame[i] = native_data_020f69c4[i];
    for (i = 0; i < 4; ++i) seed[i] = native_data_020f6044[i];
    for (i = 0; i < call_count; ++i) { ids[i] = call_ids[i]; args[i] = call_args[i]; }
    *count = call_count;
}
