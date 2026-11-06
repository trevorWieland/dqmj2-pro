typedef unsigned int u32;
u32 save_payload_checksum(const void *block) {
    u32 index = 0;
    const u32 *words = (const u32 *)((const unsigned char *)block + 0x90);
    u32 sum = index;
    for (; index < 0x1c10; index++) sum += *words++;
    return sum;
}
u32 save_header_checksum(const u32 *words) {
    u32 index = 0;
    u32 sum = index;
    for (; index < 0x23; index++) sum += *words++;
    return sum;
}
