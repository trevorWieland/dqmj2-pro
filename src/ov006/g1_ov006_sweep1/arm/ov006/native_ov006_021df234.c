/* ov006 row 0x021df234: 220 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xd8 -> native_data_0220d0dc (image word 0x0220d0dc)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021df234; the literal pool and
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

extern u8 native_data_0220d0dc[];
extern void native_fn_0203cc2c(void);
extern void native_fn_0204518c(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_02045490(void);
extern void native_fn_02045994(void);
extern void native_fn_0202a498(void);
extern void native_fn_021ddf28(void);
extern void native_fn_021dde3c(void);
extern void native_fn_021df17c(void);


asm u32 native_ov006_021df234 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r0, =native_data_0220d0dc
    mov r1, #2
    bl native_fn_0203cc2c
    mov r4, r0
    mov r2, #0
    add r0, sp, #4
    mov r1, r4
    strh r2, [sp]
    bl native_fn_0204518c
    ldr r0, [sp, #0x4]
    ldr r2, [sp, #0x8]
    mov r1, #0
    bl native_fn_0204820c
    add r0, sp, #0
    mov r1, #0
    mov r2, #2
    bl native_fn_0204820c
    bl native_fn_02048308
    mov r1, #32
    ldr r0, [sp, #0x4]
    mov r2, r1
    bl native_fn_0204820c
    bl native_fn_02048308
    add r0, sp, #4
    mov r1, r4
    mov r2, #1
    bl native_fn_0204518c
    ldr r1, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, #1
    mov r2, #0
    bl native_fn_02045490
    add r0, sp, #4
    mov r1, r4
    mov r2, #2
    ldr r5, [sp, #0x8]
    bl native_fn_0204518c
    ldr r1, [sp, #0x4]
    ldr r3, [sp, #0x8]
    mov r0, #1
    mov r2, #0
    bl native_fn_02045994
    mov r1, r4
    mov r0, #2
    bl native_fn_0202a498
    mov r1, r5
    mov r0, #1
    bl native_fn_021ddf28
    bl native_fn_021dde3c
    bl native_fn_021df17c
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
