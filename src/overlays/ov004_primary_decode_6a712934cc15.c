typedef unsigned int u32;
typedef unsigned char u8;
extern u8 DSProt_BSS[];
extern u32 func_ov004_021d7de8(u32);

u32 native_ov004_021d7e24(u32 *entry) {
    u32 *cursor;
    u32 *end;
    u32 rolling;
    u32 kind;
    u32 plain;
    u32 next;
    u8 *header;
    header = (u8 *)entry - 12;
    *(u32 *)(header + 8) = 0;
    *(u32 *)(header + 4) = 0;
    *(entry - 3) = 0;
    do {
        cursor = (u32 *)(entry[0] - 0x1000);
        end = (u32 *)((u32)cursor + (((entry[1] - (u32)DSProt_BSS - 0x1000) >> 2) << 2));
        rolling = 0xF0B9A2EA;
        while (cursor < end) {
            kind = func_ov004_021d7de8(*cursor);
            switch (kind) {
            case 1:
            case 3:
                plain = (((*cursor & 0x00FFFFFF) + 0xFFFFFBFE) & 0x00FFFFFF);
                plain = ((*cursor & 0xFF000000) ^ 0x01000000) | plain;
                *cursor = plain;
                rolling = (rolling ^ (plain >> 24)) & 0x00FFFFFF;
                break;
            case 2:
                *cursor ^= 0x01000000;
            default:
                plain = *cursor ^ rolling;
                *cursor = plain;
                rolling = (rolling ^ plain ^ (plain >> 8)) & 0x00FFFFFF;
                break;
            }
            cursor++;
        }
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
        entry[0] = entry[1] = 0;
        entry += 2;
        next = *entry;
    } while (next);
    return next;
}
