/* ov000 row 0x02208c40: 80 bytes.
 *
 * Decoded shape: 1 call, no loop.
 *
 *   pool +0x4c -> native_data_02238510 (image word 0x02238510)
 *   call +0x38 -> native_fn_02205e70
 *   test +0x0c cmp r1, #0
 *   test +0x14 cmp r1, #1
 *   test +0x1c cmp r1, #7
 *   memory +0x08 ldrb r1, [r0]
 *   memory +0x2c strb r1, [r0]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: state chain folds the two shared returns the image keeps
 * (50-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02208c40; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_02238510[];
extern void native_fn_02205e70(void);


asm u32 native_ov000_02208c40 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r0, =native_data_02238510
    ldrb r1, [r0]
    cmp r1, #0
    beq ov000_02208c40_L28
    cmp r1, #1
    beq ov000_02208c40_L44
    cmp r1, #7
    beq ov000_02208c40_L34
    b ov000_02208c40_L44
ov000_02208c40_L28:
    mov r1, #1
    strb r1, [r0]
    b ov000_02208c40_L44
ov000_02208c40_L34:
    mov r0, #0
    bl native_fn_02205e70
    mov r0, #1
    ldmia sp!, {r3, pc}
ov000_02208c40_L44:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
