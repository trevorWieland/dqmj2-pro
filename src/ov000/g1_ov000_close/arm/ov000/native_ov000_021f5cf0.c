/* ov000 row 0x021f5cf0: 228 bytes.
 *
 * What it does: 56 instructions; 10 call(s) to 0x021f6008, 0x01ffa824, 0x01ffb4ec, +7 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x021c9698 (image word 0x021c9698)
 *   back edge +0x68 -> +0x20
 *   back edge +0xcc -> +0x84
 *   test +0x64 cmp r7, #4
 *   test +0xc8 cmp r9, #4
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f5cf0; the literal pool and
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


asm u32 native_ov000_021f5cf0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #76
    bl native_fn_021f6008
    mov r7, #0
    mov r6, #2
    mov r5, r7
    mov r4, #3
    mov r8, #12
ov000_021f5cf0_L20:
    bl native_fn_01ffa824
    and r0, r0, #255
    bl native_fn_01ffb4ec
    add r0, r7, #7
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r6, [sp]
    str r5, [sp, #0x4]
    str r5, [sp, #0x8]
    mov r1, r4
    mov r2, r7, lsl #2
    add r2, r2, #7
    and r2, r2, #255
    mov r3, r8
    bl native_fn_02061c1c
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #4
    blo ov000_021f5cf0_L20
    mov r9, #0
    ldr r6, =0x021c9698
    add r8, sp, #12
    mov r7, #255
    mov r5, #31
    mov r4, r9
ov000_021f5cf0_L84:
    mov r0, r9
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
    add r0, r9, #1
    and r9, r0, #255
    cmp r9, #4
    blo ov000_021f5cf0_L84
    mov r0, #1
    bl native_fn_02045ed0
    add sp, sp, #76
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
