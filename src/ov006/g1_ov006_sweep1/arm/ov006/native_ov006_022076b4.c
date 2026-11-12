/* ov006 row 0x022076b4: 152 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> native_data_0220e984 (image word 0x0220e984)
 *   pool +0x88 -> native_data_0220c88c (image word 0x0220c88c)
 *   pool +0x8c -> constant 0x020481b8 (image word 0x020481b8)
 *   pool +0x90 -> constant 0x0204820c (image word 0x0204820c)
 *   pool +0x94 -> native_data_0220c884 (image word 0x0220c884)
 *   back edge +0x70 -> +0x40
 *   test +0x20 cmp r4, #0
 *   test +0x6c cmp r8, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022076b4; the literal pool and
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

extern u8 native_data_0220e984[];
extern void native_fn_0203cc2c(void);
extern u8 native_data_0220c88c[];
extern u8 native_data_0220c884[];
extern void native_fn_0202a498(void);


asm u32 native_ov006_022076b4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r4, r0
    ldr r0, =native_data_0220e984
    mov r1, #1
    bl native_fn_0203cc2c
    movs r6, r0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, =native_data_0220c88c
    cmp r4, #0
    ldreq r10, =0x020481b8
    add r7, r0, r4, lsl #2
    ldrne r10, =0x0204820c
    ldr r4, =native_data_0220c884
    mov r8, #0
    mov r5, #32
    mov r11, #2
ov006_022076b4_L40:
    ldrb r1, [r7, r8]
    mov r2, r5
    add r0, r6, r8, lsl #5
    mov r9, r1, lsl #5
    mov r1, r9
    blx r10
    mov r0, r4
    mov r1, r9
    mov r2, r11
    blx r10
    add r8, r8, #1
    cmp r8, #2
    blt ov006_022076b4_L40
    mov r1, r6
    mov r0, #1
    bl native_fn_0202a498
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
