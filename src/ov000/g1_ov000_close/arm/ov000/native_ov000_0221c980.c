/* ov000 row 0x0221c980: 100 bytes.
 *
 * What it does: 25 instructions; 3 call(s) to 0x0221c658, 0x0221c758, 0x0221c938; loops (back edge at +0x0c); returns through pop {r3, r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221c980; the literal pool and
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

extern void native_fn_0221c658(void);
extern void native_fn_0221c758(void);
extern void native_fn_0221c938(void);


asm u32 native_ov000_0221c980 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #20
    mov r4, r0
    bl native_fn_0221c658
    mov r3, #1
    str r3, [sp]
    mov r1, #30
    str r1, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    str r3, [sp, #0xc]
    str r3, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #0
    mov r2, #127
    bl native_fn_0221c758
    mov r0, #0
    mov r12, #8
    mov r2, r0
    mov r3, r4
    mov r1, #9
    str r12, [sp]
    bl native_fn_0221c938
    add sp, sp, #20
    ldmia sp!, {r3, r4, pc}
}
