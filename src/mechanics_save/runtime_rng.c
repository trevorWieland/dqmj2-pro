typedef unsigned int u32;
extern u32 native_rng_state;
u32 saved_runtime_random(int limit) {
    native_rng_state = native_rng_state * 0x41c64e6du + 12345;
    if (limit <= 0) return 0;
    return (native_rng_state >> 16) % (u32)limit;
}
