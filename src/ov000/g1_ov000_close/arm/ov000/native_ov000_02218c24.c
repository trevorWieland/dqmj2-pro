/* ov000 row 0x02218c24: 144 bytes.
 *
 * What it does: 35 instructions; 5 call(s) to 0x0204ad3c, 0x0204ad90, 0x0204ad3c, +2 more; loops (back edge at +0x30); returns through pop {r3, r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x8c -> constant 0x02245e54 (image word 0x02245e54)
 *   branch +0x10 -> +0x38
 *   branch +0x34 -> +0x64
 *   branch +0x70 -> +0x80
 *   test +0x0c cmp r4, #400
 *   test +0x3c cmp r0, #2
 *   test +0x6c cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218c24; the literal pool and
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

extern void native_fn_0204ad3c(void);
extern void native_fn_0204ad90(void);
extern void native_fn_0205fb90(void);
extern void native_fn_0205fbb4(void);


asm u32 native_ov000_02218c24 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    mov r4, r0
    cmp r4, #400
    bhs ov000_02218c24_L38
    mov r1, #0
    ldr r0, =0x02245e54
    str r1, [sp]
    ldr r0, [r0, #0x34]
    mov r1, r4
    mov r2, #3
    mov r3, #1
    bl native_fn_0204ad3c
    b ov000_02218c24_L64
ov000_02218c24_L38:
    bl native_fn_0204ad90
    cmp r0, #2
    mov r3, #1
    movlt r2, #2
    movge r2, #1
    ldr r0, =0x02245e54
    str r3, [sp]
    ldr r0, [r0, #0x4]
    mov r1, r4
    and r2, r2, #255
    bl native_fn_0204ad3c
ov000_02218c24_L64:
    mov r0, r4
    bl native_fn_0205fb90
    cmp r0, #0
    bne ov000_02218c24_L80
    mov r0, r4
    mov r1, #1
    bl native_fn_0205fbb4
ov000_02218c24_L80:
    mov r0, #1
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
