/* ov006 row 0x021e9218: 80 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x48 -> constant 0x02218e18 (image word 0x02218e18)
 *   pool +0x4c -> constant 0x02218d90 (image word 0x02218d90)
 *   test +0x0c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e9218; the literal pool and
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

extern void native_fn_021e7e90(void);
extern void native_fn_02049e0c(void);
extern void native_fn_0204b61c(void);
extern void native_fn_021e8044(void);


asm u32 native_ov006_021e9218 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r1
    bl native_fn_021e7e90
    cmp r0, #0
    mov r0, #0
    ldmeqia sp!, {r4, pc}
    bl native_fn_02049e0c
    ldr r0, =0x02218e18
    mov r1, #0
    bl native_fn_0204b61c
    mov r1, r4
    mov r0, #2
    bl native_fn_021e8044
    ldr r0, =0x02218d90
    mov r1, #0
    str r1, [r0, #0x4]
    mov r0, #1
    ldmia sp!, {r4, pc}
}
