/* ov006 row 0x021e6b6c: 96 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> native_data_0220d320 (image word 0x0220d320)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e6b6c; the literal pool and
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

extern u8 native_data_0220d320[];
extern void native_fn_0203cc2c(void);
extern void native_fn_021e6b40(void);
extern void native_fn_0204518c(void);
extern void native_fn_02045994(void);
extern void native_fn_0202a498(void);


asm u32 native_ov006_021e6b6c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    mov r5, r0
    ldr r0, =native_data_0220d320
    mov r1, #1
    bl native_fn_0203cc2c
    mov r4, r0
    mov r0, r5
    bl native_fn_021e6b40
    mov r2, r0
    add r0, sp, #0
    mov r1, r4
    bl native_fn_0204518c
    ldr r1, [sp]
    ldr r3, [sp, #0x4]
    mov r0, #1
    mov r2, #0
    bl native_fn_02045994
    mov r1, r4
    mov r0, #1
    bl native_fn_0202a498
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
}
