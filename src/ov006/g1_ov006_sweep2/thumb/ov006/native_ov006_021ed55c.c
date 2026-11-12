/* ov006 row 0x021ed55c: 108 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x60 -> constant 0x02219b4c (image word 0x02219b4c)
 *   pool +0x64 -> constant 0x000005dc (image word 0x000005dc)
 *   pool +0x68 -> native_data_0220d448 (image word 0x0220d448)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ed55c; the literal pool and
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

extern void native_fn_021edbac(void);
extern void native_fn_021edb9c(void);
extern u8 native_data_0220d448[];
extern void native_fn_021edcd0(void);
extern void native_fn_021ed9d4(void);
extern void native_fn_021ed6a8(void);
extern void native_fn_021ed700(void);


asm u32 native_ov006_021ed55c (register u32 a0)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0x14
    ldr r0, =0x02219b4c
    add r6, r2, #0x0
    ldr r4, [r0, #0x14]
    ldr r2, =0x000005dc
    add r5, r1, #0x0
    add r0, r4, #0x0
    mov r1, #0x0
    bl native_fn_021edbac
    add r5, #0x10
    add r0, sp, #0xc
    add r1, r5, #0x0
    mov r2, #0x8
    bl native_fn_021edb9c
    ldr r0, =native_data_0220d448
    bl native_fn_021edcd0
    add r3, r0, #0x0
    ldr r2, =native_data_0220d448
    add r0, sp, #0xc
    mov r1, #0x8
    bl native_fn_021ed9d4
    mov r2, #0x0
    mov r1, #0x3
    str r2, [sp]
    mov r0, #0x11
    str r0, [sp, #0x4]
    add r0, sp, #0xc
    str r0, [sp, #0x8]
    add r0, r4, #0x0
    lsl r1, r1, #0xc
    add r3, r2, #0x0
    bl native_fn_021ed6a8
    add r0, r4, #0x0
    mov r1, #0x18
    mov r2, #0x0
    add r3, r6, #0x0
    bl native_fn_021ed700
    mov r0, #0x0
    add sp, #0x14
    pop {r3, r4, r5, r6, pc}
    mov r8, r8
}
