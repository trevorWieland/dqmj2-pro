/* ov001 row 0x02206764: 240 bytes.
 *
 * What it does: 60 instructions; 4 call(s) to 0x02204250, 0x0220684c, 0x02206700, +1 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, pc}
 *
 * Decoded shape: loop with 4 calls (60 instructions, 4 calls, 4 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x24 -> +0x50
 *   branch +0x38 -> +0x58
 *   branch +0x4c -> +0x58
 *   branch +0x60 -> +0xe8
 *   branch +0x74 -> +0x90
 *   test +0x10 cmp r0, #0
 *   test +0x20 cmp r0, #127
 *   test +0x34 cmp r2, r1
 *   test +0x5c cmp r0, #0
 *   test +0x70 cmp r1, #0
 *   test +0x98 cmp r0, #0
 *   test +0xc4 cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02206764; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02204250(void);
extern void native_fn_02206700(void);


asm u32 native_ov001_02206764 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    ldrb r0, [r5, #0x23]
    ldrsh r4, [r5, #20]
    cmp r0, #0
    moveq r0, #1
    ldmeqia sp!, {r3, r4, r5, pc}
    ldrsb r0, [r5, #8]
    cmp r0, #127
    beq ov001_02206764_L50
    bl native_fn_02204250
    ldrsb r1, [r0, #36]
    ldr r2, [r5, #0x2c]
    cmp r2, r1
    beq ov001_02206764_L58
    mov r1, #8
    strh r1, [r5, #26]
    ldrsb r0, [r0, #36]
    str r0, [r5, #0x2c]
    b ov001_02206764_L58
ov001_02206764_L50:
    mov r0, #1
    str r0, [r5, #0x2c]
ov001_02206764_L58:
    ldr r0, [r5, #0x2c]
    cmp r0, #0
    ble ov001_02206764_Le8
    ldrsh r1, [r5, #38]
    sub r0, r1, #1
    strh r0, [r5, #38]
    cmp r1, #0
    bgt ov001_02206764_L90
    ldr r1, [r5, #0x30]
    mov r0, #15
    add r1, r1, #1
    and r1, r1, #1
    str r1, [r5, #0x30]
    strh r0, [r5, #38]
ov001_02206764_L90:
    ldr r0, [r5, #0x30]
    mov r2, r4
    cmp r0, #0
    moveq r0, #166
    movne r0, #164
    and r1, r0, #255
    str r1, [sp]
    mov r0, r5
    mov r1, #0
    mov r3, #7
    bl native_fn_02206700
    ldr r0, [r5, #0x30]
    add r2, r4, #20
    cmp r0, #0
    moveq r0, #167
    movne r0, #165
    and r12, r0, #255
    mov r0, r5
    mov r1, #3
    mov r3, #7
    str r12, [sp]
    bl native_fn_02206700
ov001_02206764_Le8:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
