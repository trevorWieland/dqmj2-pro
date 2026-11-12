/* ov000 row 0x021da08c: 224 bytes.
 *
 * What it does: 53 instructions; 8 call(s) to 0x021df1d0, 0x021da0d4, 0x021d9b34, +5 more; loops (back edge at +0x40); returns through pop {r3, r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd4 -> constant 0x00004650 (image word 0x00004650)
 *   pool +0xd8 -> constant 0x00002a30 (image word 0x00002a30)
 *   pool +0xdc -> constant 0x0000286e (image word 0x0000286e)
 *   branch +0x14 -> +0xc8
 *   branch +0x20 -> +0xbc
 *   branch +0x2c -> +0x48
 *   branch +0x44 -> +0xbc
 *   branch +0x50 -> +0xbc
 *   branch +0x5c -> +0x7c
 *   branch +0x78 -> +0xbc
 *   branch +0x84 -> +0xa4
 *   branch +0xa0 -> +0xbc
 *   test +0x10 cmp r0, #0
 *   test +0x1c cmp r4, r0
 *   test +0x28 cmp r4, r1
 *   test +0x4c cmp r4, r0
 *   test +0x58 cmp r4, r0
 *   test +0x80 cmp r4, r1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021da08c; the literal pool and
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

extern void native_fn_021df1d0(void);
extern void native_fn_021d9b34(void);


asm u32 native_ov000_021da08c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    mov r4, r0
    bl native_fn_021df1d0
    cmp r0, #0
    beq ov000_021da08c_Lc8
    ldr r0, =0x00004650
    cmp r4, r0
    bhs ov000_021da08c_Lbc
    ldr r1, =0x00002a30
    cmp r4, r1
    blo ov000_021da08c_L48
    mov r3, #2
    mov r0, r4
    mov r2, r1
    str r3, [sp]
    bl native_fn_021d9b34
    b ov000_021da08c_Lbc
ov000_021da08c_L48:
    sub r0, r1, #1
    cmp r4, r0
    bhs ov000_021da08c_Lbc
    sub r0, r1, #150
    cmp r4, r0
    blo ov000_021da08c_L7c
    sub r1, r1, #150
    mov r3, #1
    mov r0, r4
    mov r2, r1
    str r3, [sp]
    bl native_fn_021d9b34
    b ov000_021da08c_Lbc
ov000_021da08c_L7c:
    ldr r1, =0x0000286e
    cmp r4, r1
    blo ov000_021da08c_La4
    mov r12, #1
    mov r0, r4
    add r2, r1, #300
    mov r3, #0
    str r12, [sp]
    bl native_fn_021d9b34
    b ov000_021da08c_Lbc
ov000_021da08c_La4:
    mov r1, #0
    mov r0, r4
    mov r2, r1
    mov r3, r1
    str r1, [sp]
    bl native_fn_021d9b34
ov000_021da08c_Lbc:
    add sp, sp, #4
    mov r0, #1
    ldmia sp!, {r3, r4, pc}
ov000_021da08c_Lc8:
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
