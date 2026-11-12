/* ov000 row 0x021fedf0: 280 bytes.
 *
 * What it does: 67 instructions; 7 call(s) to 0x02215698, 0x02217440, 0x022163fc, +4 more; no back edge; returns through pop {r3, r4, r5, r6, r7, r8, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x10c -> constant 0x02237564 (image word 0x02237564)
 *   pool +0x110 -> constant 0x0223756c (image word 0x0223756c)
 *   pool +0x114 -> constant 0x0223765c (image word 0x0223765c)
 *   branch +0x1c -> +0x2c
 *   branch +0x24 -> +0x88
 *   branch +0x28 -> +0xfc
 *   branch +0x84 -> +0xfc
 *   test +0x18 cmp r4, #1
 *   test +0x20 cmp r4, #3
 *   2 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fedf0; the literal pool and
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

extern void native_fn_02215698(void);
extern void native_fn_02217440(void);
extern void native_fn_022163fc(void);
extern void native_fn_02216440(void);
extern void native_fn_02216260(void);
extern void native_fn_02216350(void);
extern void native_fn_021fefdc(void);


asm u32 native_ov000_021fedf0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #20
    mov r4, r0
    bl native_fn_02215698
    bl native_fn_02217440
    mov r3, r0
    cmp r4, #1
    beq ov000_021fedf0_L2c
    cmp r4, #3
    beq ov000_021fedf0_L88
    b ov000_021fedf0_Lfc
ov000_021fedf0_L2c:
    ldr r0, =0x02237564
    ldr r5, =0x0223756c
    ldrb r1, [r0, #0x1ec]
    mov r0, #5
    ldmia r5, {r7, r8}
    add r1, r1, #1
    and r6, r1, #255
    mov r2, r0
    mov r1, #0
    bl native_fn_022163fc
    str r6, [sp]
    str r6, [sp, #0x4]
    mov r1, #1
    str r1, [sp, #0x8]
    mov r0, #15
    str r0, [sp, #0xc]
    mov r0, r5
    str r1, [sp, #0x10]
    mov r2, #3
    mov r3, #28
    bl native_fn_02216440
    stmia r5, {r7, r8}
    b ov000_021fedf0_Lfc
ov000_021fedf0_L88:
    mov r0, #3
    str r0, [sp]
    mov r0, #30
    str r0, [sp, #0x4]
    mov r2, #2
    mov r0, #1
    str r2, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r0, [sp, #0x10]
    ldrsb r1, [r3, #16]
    mov r3, r0
    ldr r5, =0x0223765c
    bl native_fn_02216260
    mov r0, #10
    str r0, [sp]
    mov r2, #5
    str r2, [sp, #0x4]
    mov r0, r5
    str r2, [sp, #0x8]
    mov r12, #0
    mov r1, #1
    mov r3, #28
    str r12, [sp, #0xc]
    bl native_fn_02216350
    ldr r0, =0x02237564
    ldr r0, [r0, #0x1e8]
    ldrb r0, [r0, #0x32]
    str r0, [r5]
ov000_021fedf0_Lfc:
    mov r0, r4
    bl native_fn_021fefdc
    add sp, sp, #20
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
