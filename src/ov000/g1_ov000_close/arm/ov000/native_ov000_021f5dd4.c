/* ov000 row 0x021f5dd4: 220 bytes.
 *
 * What it does: 54 instructions; 10 call(s) to 0x021f6008, 0x01ffa824, 0x01ffb4ec, +7 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd8 -> constant 0x021c9698 (image word 0x021c9698)
 *   back edge +0x64 -> +0x24
 *   back edge +0xc4 -> +0x80
 *   test +0x60 cmp r6, #8
 *   test +0xc0 cmp r9, #8
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f5dd4; the literal pool and
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

extern void native_fn_021f6008(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffb4ec(void);
extern void native_fn_02061c1c(void);
extern void native_fn_02046af4(void);
extern void native_fn_01ffb648(void);
extern void native_fn_02045ed0(void);


asm u32 native_ov000_021f5dd4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #76
    bl native_fn_021f6008
    mov r6, #0
    mov r7, #5
    mov r5, #2
    mov r4, r6
    mov r9, #3
    mov r8, #12
ov000_021f5dd4_L24:
    bl native_fn_01ffa824
    and r0, r0, #255
    bl native_fn_01ffb4ec
    str r5, [sp]
    str r4, [sp, #0x4]
    str r4, [sp, #0x8]
    add r0, r6, #7
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r9
    and r2, r7, #255
    mov r3, r8
    bl native_fn_02061c1c
    add r7, r7, #2
    add r6, r6, #1
    cmp r6, #8
    blt ov000_021f5dd4_L24
    mov r9, #0
    ldr r6, =0x021c9698
    add r8, sp, #12
    mov r7, #255
    mov r5, #31
    mov r4, r9
ov000_021f5dd4_L80:
    and r0, r9, #255
    bl native_fn_01ffb4ec
    mov r1, r0
    add r0, r1, #256
    ldrsb r10, [r0, #101]
    mov r0, r6
    mov r2, r5
    str r8, [sp]
    str r7, [sp, #0x4]
    mov r3, r4
    bl native_fn_02046af4
    add r0, r10, #7
    mov r1, r8
    and r0, r0, #255
    bl native_fn_01ffb648
    add r9, r9, #1
    cmp r9, #8
    blt ov000_021f5dd4_L80
    mov r0, #1
    bl native_fn_02045ed0
    add sp, sp, #76
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
