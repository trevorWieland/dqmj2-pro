/* ov001 row 0x02207074: 308 bytes.
 *
 * What it does: 76 instructions; 9 call(s) to 0x022068a0, 0x021fe4ac, 0x02204c1c, +6 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (76 instructions, 9 calls, 0 branches, 9 back edges, 1 literal slot).
 *
 *   pool +0x130 -> native_data_0222f028 (image word 0x0222f028)
 *   test +0x24 cmp r0, #0
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02207074; the literal pool and
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

extern void native_fn_022068a0(void);
extern u8 native_data_0222f028[];
extern void native_fn_021fe4ac(void);
extern void native_fn_02204c1c(void);
extern void native_fn_021fe738(void);
extern void native_fn_0204a574(void);
extern void native_fn_02065818(void);
extern void native_fn_02202320(void);
extern void native_fn_021fe6b8(void);
extern void native_fn_0206006c(void);


asm u32 native_ov001_02207074 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #24
    bl native_fn_022068a0
    add r2, sp, #20
    mov r1, #0
    mov r5, r0
    strh r1, [r2]
    strh r1, [r2, #2]
    ldrsb r0, [r5, #145]
    cmp r0, #0
    addne sp, sp, #24
    ldmneia sp!, {r3, r4, r5, r6, r7, pc}
    ldr r4, =native_data_0222f028
    mov r12, #1
    ldrb r6, [r4, #0xe]
    ldrb r7, [r4, #0xf]
    mov r0, #6
    mov r3, r6
    str r7, [sp]
    ldrb lr, [r4, #0x10]
    mov r1, #8
    mov r2, #31
    str lr, [sp, #0x4]
    ldrb r4, [r4, #0x11]
    str r4, [sp, #0x8]
    str r12, [sp, #0xc]
    str r12, [sp, #0x10]
    bl native_fn_021fe4ac
    add r1, r7, #1
    mov r1, r1, lsl #19
    str r0, [r5, #0x8]
    mov r2, r1, asr #16
    mov r0, #0
    mov r1, #176
    mov r3, #3
    bl native_fn_02204c1c
    strb r0, [r5, #0x92]
    mov r1, #1
    mov r0, #12
    strb r1, [r5, #0x91]
    bl native_fn_021fe738
    mov r4, r0
    mov r0, #24
    strh r0, [sp, #20]
    mov r0, #42
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    mov r0, #6
    add r1, sp, #20
    mov r2, #5
    mov r3, #2
    bl native_fn_0204a574
    add r1, r6, #2
    mov r1, r1, lsl #24
    mov r2, r7, lsl #24
    mov r0, r4
    mov r1, r1, asr #24
    mov r2, r2, asr #24
    bl native_fn_02065818
    ldr r0, [r5, #0x8]
    ldr r1, [r0]
    ldrsb r0, [r0, #5]
    ldr r4, [r1, #0x4]
    bl native_fn_02202320
    bl native_fn_021fe6b8
    ldrsb r1, [r4, #31]
    str r1, [sp]
    ldrsb r1, [r4, #28]
    ldrsb r2, [r4, #29]
    ldrsb r3, [r4, #30]
    bl native_fn_0206006c
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
