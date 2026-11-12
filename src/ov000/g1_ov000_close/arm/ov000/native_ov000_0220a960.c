/* ov000 row 0x0220a960: 172 bytes.
 *
 * What it does: 43 instructions and 1 call(s), then a 11-entry dispatch through an inline branch table at 0x0220a970 (dispatch word at 0x0220a968)
 *
 * Carrier: mwccarm asm with dcd data runs.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles, the meaning of the table entries and every callee contract are not established by byte identity; the dispatch range and the table bounds are measured.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_020c56b4(void);


asm u32 native_ov000_0220a960 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r1, #10
    addls pc, pc, r1, lsl #2
    b L_0220aa04
    dcd 0xea000009
    dcd 0xea00000a
    dcd 0xea00000b
    dcd 0xea00000c
    dcd 0xea00000d
    dcd 0xea00000e
    dcd 0xea000015
    dcd 0xea00001c
    dcd 0xea000015
    dcd 0xea000016
    dcd 0xea000017
    mov r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #40960
    ldmia sp!, {r3, pc}
    add r0, r0, #512
    ldrsh r0, [r0, #118]
    bl native_fn_020c56b4
    ldrb r0, [r0, #0x6]
    cmp r0, #4
    moveq r0, #40960
    movne r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #8192
    ldmia sp!, {r3, pc}
    mov r0, #81920
    ldmia sp!, {r3, pc}
    mov r0, #8192
    ldmia sp!, {r3, pc}
L_0220aa04:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
