/* ov000 row 0x0221ca0c: 116 bytes.
 *
 * What it does: 29 instructions; 6 call(s) to 0x0221c658, 0x0221c758, 0x02049ad0, +3 more; loops (back edge at +0x08); returns through pop {r3, r4, pc}
 *
 * Decoded shape: block fill.
 *
 *   1 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221ca0c; the literal pool and
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
extern void native_fn_02049ad0(void);
extern void native_fn_02049f4c(void);
extern void native_fn_02062b0c(void);
extern void native_fn_0221c820(void);


asm u32 native_ov000_0221ca0c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #20
    bl native_fn_0221c658
    mov r1, #21
    mov r3, r0
    mov r2, #2
    str r1, [sp]
    mov r0, #28
    stmib sp, {r0, r2}
    mov r0, #0
    str r0, [sp, #0xc]
    mov r0, #1
    str r0, [sp, #0x10]
    ldrsb r1, [r3, #16]
    mov r3, r2
    bl native_fn_0221c758
    mov r0, #1
    bl native_fn_02049ad0
    ldr r1, [r0]
    ldr r4, [r1, #0x4]
    bl native_fn_02049f4c
    bl native_fn_02062b0c
    mov r1, r0
    mov r0, r4
    mov r2, #16
    mov r3, #0
    bl native_fn_0221c820
    add sp, sp, #20
    ldmia sp!, {r3, r4, pc}
}
