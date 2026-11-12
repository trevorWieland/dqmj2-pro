/* ov000 row 0x021f4c44: 288 bytes.
 *
 * What it does: 71 instructions; 8 call(s) to 0x02061c1c, 0x021f4c64, 0x02061c1c, +5 more; loops (back edge at +0x44); returns through pop {r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x11c -> constant 0x04000008 (image word 0x04000008)
 *   back edge +0x54 -> +0x20
 *   test +0x4c cmp r6, #8
 *   1 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f4c44; the literal pool and
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

extern void native_fn_02061c1c(void);
extern void native_fn_01ffb50c(void);
extern void native_fn_02045ed0(void);
extern void native_fn_021f4dac(void);


asm u32 native_ov000_021f4c44 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    mov r6, #0
    mov r7, #7
    mov r5, #2
    mov r4, r6
    mov r9, #11
    mov r8, #12
ov000_021f4c44_L20:
    add r0, r6, #6
    str r5, [sp]
    mov r0, r0, lsl #24
    str r4, [sp, #0x4]
    mov r1, r9
    mov r3, r8
    mov r0, r0, asr #24
    and r2, r7, #255
    str r4, [sp, #0x8]
    bl native_fn_02061c1c
    add r6, r6, #1
    cmp r6, #8
    add r7, r7, #2
    blt ov000_021f4c44_L20
    mov r0, #2
    str r0, [sp]
    mov r4, #0
    str r4, [sp, #0x4]
    mov r0, #14
    mov r1, #11
    mov r2, #5
    mov r3, #6
    str r4, [sp, #0x8]
    bl native_fn_02061c1c
    mov r0, #14
    mov r1, #16
    mov r2, #13
    mov r3, #4
    str r4, [sp]
    bl native_fn_01ffb50c
    mov r0, #2
    stmia sp, {r0, r4}
    mov r0, #15
    mov r1, #9
    mov r2, #1
    mov r3, #14
    str r4, [sp, #0x8]
    bl native_fn_02061c1c
    mov r1, #1
    str r1, [sp]
    mov r0, #15
    mov r1, #16
    mov r2, #13
    mov r3, #3
    bl native_fn_01ffb50c
    mov r0, #1
    bl native_fn_02045ed0
    bl native_fn_021f4dac
    ldr r1, =0x04000008
    ldrh r0, [r1]
    bic r0, r0, #3
    orr r0, r0, #2
    strh r0, [r1]
    ldrh r0, [r1, #4]
    bic r0, r0, #3
    orr r0, r0, #1
    strh r0, [r1, #4]
    ldrh r0, [r1, #6]
    bic r0, r0, #3
    orr r0, r0, #3
    strh r0, [r1, #6]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
