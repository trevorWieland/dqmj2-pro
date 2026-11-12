/* ov006 row 0x02204cb4: 112 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204cb4; the literal pool and
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

extern void native_fn_021e6488(void);
extern void native_fn_021eb9a4(void);
extern void native_fn_021e71e4(void);
extern void native_fn_0207e97c(void);
extern void native_fn_02008d78(void);
extern void native_fn_02063aa4(void);
extern void native_fn_0207e720(void);
extern void native_fn_021e7a18(void);
extern void native_fn_0207e874(void);


asm u32 native_ov006_02204cb4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #16
    bl native_fn_021e6488
    mov r1, #0
    mov r2, r1
    mov r0, #3
    bl native_fn_021eb9a4
    bl native_fn_021e71e4
    bl native_fn_0207e97c
    add r0, sp, #0
    mov r1, #0
    mov r2, #16
    bl native_fn_02008d78
    mov r0, #0
    strb r0, [sp]
    mov r0, #16
    strb r0, [sp, #0xc]
    bl native_fn_02063aa4
    str r0, [sp, #0x8]
    mov r0, #1
    strb r0, [sp, #0xd]
    add r0, sp, #0
    bl native_fn_0207e720
    mov r0, #0
    bl native_fn_021e7a18
    bl native_fn_0207e874
    add sp, sp, #16
    ldmia sp!, {r3, pc}
}
