/* ov006 row 0x02204bc8: 120 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204bc8; the literal pool and
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

extern void native_fn_020633b0(void);
extern void native_fn_021e6488(void);
extern void native_fn_021eb9a4(void);
extern void native_fn_021e71e4(void);
extern void native_fn_0207e97c(void);
extern void native_fn_0207e7e4(void);
extern void native_fn_021e7a18(void);
extern void native_fn_0207e874(void);
extern void native_fn_021e6e70(void);


asm u32 native_ov006_02204bc8 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    mov r4, r0
    bl native_fn_020633b0
    mov r0, r4
    bl native_fn_021e6488
    mov r1, #0
    mov r2, r1
    mov r0, #3
    bl native_fn_021eb9a4
    bl native_fn_021e71e4
    bl native_fn_0207e97c
    mov r2, #0
    mov r3, #1
    mov r1, #12
    add r0, sp, #0
    strb r1, [sp, #0xc]
    strb r3, [sp]
    strh r2, [sp, #2]
    strb r2, [sp, #0x4]
    strb r2, [sp, #0x5]
    str r2, [sp, #0x8]
    strb r3, [sp, #0xd]
    bl native_fn_0207e7e4
    mov r0, #0
    bl native_fn_021e7a18
    bl native_fn_0207e874
    bl native_fn_021e6e70
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
