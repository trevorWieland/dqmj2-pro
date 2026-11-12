/* ov000 row 0x0222b3ec: 256 bytes.
 *
 * What it does: 63 instructions; 5 call(s) to 0x0222b24c, 0x0222b4ac, 0x0222b24c, +2 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xfc -> constant 0x02247704 (image word 0x02247704)
 *   branch +0x6c -> +0xc0
 *   back edge +0xbc -> +0x7c
 *   test +0x5c cmp r10, #0
 *   test +0xb8 cmp r6, r10
 *   1 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0222b3ec; the literal pool and
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

extern void native_fn_0222b24c(void);
extern void native_fn_0222b2e8(void);


asm u32 native_ov000_0222b3ec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    ldr r7, [sp, #0x44]
    mov r10, r1
    ldr r8, [sp, #0x40]
    mov r1, r10, lsl #1
    add r2, r7, #2
    str r0, [sp, #0x14]
    and r0, r2, #255
    str r8, [sp]
    add r1, r1, #2
    str r0, [sp, #0x4]
    and r0, r1, #255
    str r0, [sp, #0x8]
    mov r0, #1
    mov r9, r3
    str r0, [sp, #0xc]
    mov r1, #0
    mov r2, #12
    str r1, [sp, #0x10]
    bl native_fn_0222b24c
    add r1, r9, #1
    add r0, r8, #1
    cmp r10, #0
    and r9, r1, #255
    and r8, r0, #255
    mov r6, #0
    bls ov000_0222b3ec_Lc0
    mov r5, #2
    mov r11, r6
    mov r4, #1
ov000_0222b3ec_L7c:
    add r0, r8, r6, lsl #1
    and r0, r0, #255
    stmia sp, {r0, r7}
    add r0, r6, #3
    str r5, [sp, #0x8]
    mov r0, r0, lsl #24
    str r11, [sp, #0xc]
    mov r1, r11
    mov r2, r4
    mov r3, r9
    mov r0, r0, asr #24
    str r4, [sp, #0x10]
    bl native_fn_0222b24c
    add r0, r6, #1
    and r6, r0, #255
    cmp r6, r10
    blo ov000_0222b3ec_L7c
ov000_0222b3ec_Lc0:
    mov r3, #0
    str r3, [sp]
    mov r4, #1
    ldr r0, [sp, #0x14]
    mov r1, r10
    mov r2, r10
    mov r3, #3
    str r4, [sp, #0x4]
    bl native_fn_0222b2e8
    ldr r0, =0x02247704
    strb r9, [r0, #0x4]
    strb r8, [r0, #0x5]
    strb r7, [r0]
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
