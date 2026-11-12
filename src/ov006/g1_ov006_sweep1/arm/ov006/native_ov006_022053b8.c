/* ov006 row 0x022053b8: 156 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x94 -> native_data_0220bbd0 (image word 0x0220bbd0)
 *   pool +0x98 -> native_data_0220bbd8 (image word 0x0220bbd8)
 *   1 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022053b8; the literal pool and
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
extern void native_fn_021eb1b0(void);
extern u8 native_data_0220bbd0[];
extern u8 native_data_0220bbd8[];
extern void native_fn_021e81e8(void);
extern void native_fn_020685f0(void);
extern void native_fn_021e92b0(void);
extern void native_fn_021e7824(void);


asm u32 native_ov006_022053b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #20
    mov r4, r1
    bl native_fn_021e6488
    mov r1, #0
    mov r2, r1
    mov r0, #13
    bl native_fn_021eb9a4
    mov r0, r4
    bl native_fn_021eb1b0
    mov r0, #23
    str r0, [sp]
    mov r1, #0
    str r1, [sp, #0x4]
    mov r0, #1
    str r0, [sp, #0x8]
    str r1, [sp, #0xc]
    str r1, [sp, #0x10]
    mov r0, #2
    ldr r1, =native_data_0220bbd0
    ldr r3, =native_data_0220bbd8
    mov r2, r0
    bl native_fn_021e81e8
    mov r0, r4
    bl native_fn_020685f0
    mov r4, r0
    mov r0, #1
    bl native_fn_021e92b0
    mov r3, #0
    str r3, [sp]
    mov r2, #1
    stmib sp, {r2, r3}
    mov r1, r4
    mov r2, #2
    bl native_fn_021e7824
    add sp, sp, #20
    ldmia sp!, {r3, r4, pc}
}
