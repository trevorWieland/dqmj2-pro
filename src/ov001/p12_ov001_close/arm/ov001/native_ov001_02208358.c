/* ov001 row 0x02208358: 176 bytes.
 *
 * What it does: 44 instructions; 5 call(s) to 0x02207938, 0x020656c0, 0x022083f8, +2 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, pc}
 *
 * Decoded shape: loop with 5 calls (44 instructions, 5 calls, 3 branches, 4 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0x60
 *   branch +0x48 -> +0x60
 *   branch +0x5c -> +0xa0
 *   branch +0x64 -> +0xa0
 *   test +0x38 cmp r0, #1
 *   test +0x44 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x60 cmp r6, #100
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02208358; the literal pool and
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

extern void native_fn_02207938(void);
extern void native_fn_020656c0(void);
extern void native_fn_021fe738(void);
extern void native_fn_02065818(void);


asm u32 native_ov001_02208358 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #4
    bl native_fn_02207938
    mov r4, r0
    ldr r1, [r4, #0x8]
    ldr r0, [r4, #0x10]
    ldr r1, [r1]
    ldrb r6, [r0, #0x1fc]
    ldr r5, [r1, #0x4]
    add r1, sp, #0
    mov r0, #0
    strh r0, [r1]
    strh r0, [r1, #2]
    ldr r0, [r4, #0x24]
    cmp r0, #1
    bne ov001_02208358_L60
    bl native_fn_020656c0
    cmp r0, #0
    bne ov001_02208358_L60
    ldr r0, [r4, #0x10]
    add r0, r0, #512
    ldrsb r0, [r0, #86]
    cmp r0, #0
    beq ov001_02208358_La0
ov001_02208358_L60:
    cmp r6, #100
    blt ov001_02208358_La0
    ldrb r1, [r5, #0x1c]
    mov r0, #9
    add r1, r1, #4
    strh r1, [sp]
    ldrb r1, [r5, #0x1d]
    strh r1, [sp, #2]
    bl native_fn_021fe738
    ldrsh r1, [sp]
    ldrsh r2, [sp, #2]
    mov r1, r1, lsl #24
    mov r2, r2, lsl #24
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_02065818
ov001_02208358_La0:
    mov r0, #3
    str r0, [r4, #0x1c]
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, pc}
}
