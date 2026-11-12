/* ov000 row 0x021d7e58: 160 bytes.
 *
 * What it does: 38 instructions; 6 call(s) to 0x0202a37c, 0x021d7da4, 0x02048a9c, +3 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x98 -> constant 0x022300c0 (image word 0x022300c0)
 *   pool +0x9c -> constant 0x02230120 (image word 0x02230120)
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d7e58; the literal pool and
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

extern void native_fn_0202a37c(void);
extern void native_fn_021d7da4(void);
extern void native_fn_02048a9c(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048644(void);


asm u32 native_ov000_021d7e58 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r3, =0x022300c0
    mov r7, r0
    ldrb r4, [r3]
    mov r9, r1
    ldr r5, =0x02230120
    mov r8, r2
    add r6, r4, #1
    strb r6, [r3]
    mov r0, #2
    mov r1, #144
    mov r2, #4
    add r6, r5, r4, lsl #3
    bl native_fn_0202a37c
    str r0, [r5, r4, lsl #3]
    bl native_fn_021d7da4
    ldr r0, [r5, r4, lsl #3]
    mov r1, #0
    bl native_fn_02048a9c
    ldr r0, [r5, r4, lsl #3]
    mov r1, #0
    bl native_fn_02048a94
    ldr r3, [r5, r4, lsl #3]
    mov r7, r7, lsl #3
    ldr r0, [r3, #0x7c]
    mov r2, r9, lsl #3
    orr r0, r0, #2
    str r0, [r3, #0x7c]
    ldr r0, [r5, r4, lsl #3]
    mov r1, r7
    bl native_fn_02048a60
    ldr r1, =0x022300c0
    ldr r0, [r5, r4, lsl #3]
    ldr r1, [r1, #0x20]
    mov r2, r8
    bl native_fn_02048644
    str r7, [r6, #0x4]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
