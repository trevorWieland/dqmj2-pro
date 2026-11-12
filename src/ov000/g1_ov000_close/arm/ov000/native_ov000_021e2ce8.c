/* ov000 row 0x021e2ce8: 228 bytes.
 *
 * What it does: 51 instructions; 6 call(s) to 0x02002618, 0x02025a28, 0x02025578, +3 more; loops (back edge at +0x60); returns through pop {r4, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xcc -> constant 0x022324d4 (image word 0x022324d4)
 *   pool +0xd0 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0xd4 -> constant 0x022324c8 (image word 0x022324c8)
 *   pool +0xd8 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0xdc -> constant 0x45800000 (image word 0x45800000)
 *   pool +0xe0 -> constant 0x022324bc (image word 0x022324bc)
 *   5 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2ce8; the literal pool and
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

extern void native_fn_02002618(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_020280fc(void);
extern void native_fn_021e0d78(void);
extern void native_fn_021e1c4c(void);


asm u32 native_ov000_021e2ce8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #24
    ldr r3, =0x022324d4
    mov r4, r1
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr lr, =0x02232344
    ldr r3, =0x022324c8
    ldmia lr, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r1, =0x022322d4
    ldmia lr, {r3, r12}
    ldr r2, [r1, #0x200]
    add r0, sp, #12
    sub r2, r3, r2
    str r2, [sp, #0xc]
    ldr r2, [r1, #0x204]
    ldr r3, [lr, #0x8]
    sub r2, r12, r2
    str r2, [sp, #0x10]
    ldr r2, [r1, #0x208]
    mov r1, r0
    sub r2, r3, r2
    str r2, [sp, #0x14]
    bl native_fn_02002618
    mov r0, r4
    bl native_fn_02025a28
    ldr r1, =0x45800000
    bl native_fn_02025578
    mov r2, r0
    ldr r0, =0x022324bc
    add r1, sp, #12
    bl native_fn_020280fc
    mov r0, #1
    mov r1, #0
    mov r2, r0
    bl native_fn_021e0d78
    mov r2, #0
    str r2, [sp]
    str r2, [sp, #0x4]
    mov r0, #2
    mov r1, #1
    mov r3, r2
    str r2, [sp, #0x8]
    bl native_fn_021e1c4c
    ldr r1, =0x022322d4
    mov r2, #1
    mov r0, #0
    strb r2, [r1, #0x27f]
    add sp, sp, #24
    ldmia sp!, {r4, pc}
}
