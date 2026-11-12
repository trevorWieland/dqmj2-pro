/* ov006 row 0x021dd3c0: 96 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x5c -> native_data_0220d000 (image word 0x0220d000)
 *   branch +0x24 -> +0x54
 *   test +0x3c cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dd3c0; the literal pool and
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

extern void native_fn_02044f9c(void);
extern void native_fn_0202a37c(void);
extern u8 native_data_0220d000[];
extern void native_fn_0202a818(void);
extern void native_fn_0202a498(void);


asm u32 native_ov006_021dd3c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r2
    bl native_fn_02044f9c
    mov r5, r0
    mov r0, r6
    mov r1, #400
    mov r2, #4
    bl native_fn_0202a37c
    movs r4, r0
    beq ov006_021dd3c0_L54
    mov r2, #400
    mul r3, r5, r2
    ldr r0, =native_data_0220d000
    mov r1, r4
    bl native_fn_0202a818
    cmp r0, #0
    movne r0, r4
    ldmneia sp!, {r4, r5, r6, pc}
    mov r0, r6
    mov r1, r4
    bl native_fn_0202a498
ov006_021dd3c0_L54:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
