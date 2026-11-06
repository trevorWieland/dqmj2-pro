typedef unsigned int u32;
typedef unsigned char u8;
extern u8 DSProt_BSS[];
extern u32 func_ov004_021d8da0(void *, void *, void *, u32);

u32 native_ov004_021d8014(u32 key_reference, u32 target_reference, u32 size_reference) {
    u32 key[4];
    void *target;
    target = (void *)target_reference;
    target -= 0x1000;
    size_reference -= (u32)DSProt_BSS + 0x1000;
    key_reference -= (u32)DSProt_BSS + 0x1000;
    key_reference += target_reference & 0xFFFF;
    key[0] = key_reference ^ size_reference;
    key[1] = ((key_reference << 8) | (key_reference >> 24)) ^ size_reference;
    key[2] = ((key_reference << 16) | (key_reference >> 16)) ^ size_reference;
    key[3] = ((key_reference << 24) | (key_reference >> 8)) ^ size_reference;
    func_ov004_021d8da0(key, target, target, size_reference);
    asm {
        mov r12, #0
        mov r1, #0
    cache_segment:
        mov r0, #0
    cache_index:
        orr r2, r1, r0
        mcr p15, 0, r12, c7, c10, 4
        mcr p15, 0, r2, c7, c14, 2
        add r0, r0, #32
        cmp r0, #0x400
        blt cache_index
        add r1, r1, #0x40000000
        cmp r1, #0
        bne cache_segment
        mov r0, #0
        mcr p15, 0, r0, c7, c5, 0
        mcr p15, 0, r12, c7, c10, 4
    }
    return key_reference + ((u32)DSProt_BSS + 0x1000);
}
