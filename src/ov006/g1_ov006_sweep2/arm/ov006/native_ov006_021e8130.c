/* ov006 row 0x021e8130: 108 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e8130; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021e92cc(void);
extern void native_fn_021e75ec(void);
extern void native_fn_021e7b64(void);
extern void native_fn_021e791c(void);


asm u32 native_ov006_021e8130 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, lr}
    sub sp, sp, #12
    mov r4, r0
    mov r7, r1
    mov r6, r2
    bl native_fn_021e92cc
    movs r5, r0
    addeq sp, sp, #12
    ldmeqia sp!, {r4, r5, r6, r7, pc}
    mov r0, r4
    bl native_fn_021e75ec
    mov r0, r4
    bl native_fn_021e7b64
    mov r0, #12
    ldrb r2, [r5, #0x1e]
    mla r1, r7, r0, r6
    sub r0, r2, #2
    str r0, [sp]
    mov r2, #1
    mov r0, r4
    str r2, [sp, #0x4]
    mov r3, #0
    mov r2, #2
    str r3, [sp, #0x8]
    bl native_fn_021e791c
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, pc}
}
