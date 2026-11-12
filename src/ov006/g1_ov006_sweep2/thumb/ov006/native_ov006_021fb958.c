/* ov006 row 0x021fb958: 104 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x48 -> native_data_0220def8 (image word 0x0220def8)
 *   pool +0x4c -> constant 0x02004fd8 (image word 0x02004fd8)
 *   pool +0x50 -> native_data_0220df10 (image word 0x0220df10)
 *   pool +0x54 -> constant 0x020048a0 (image word 0x020048a0)
 *   pool +0x58 -> native_data_0220df28 (image word 0x0220df28)
 *   pool +0x5c -> constant 0x02004cd8 (image word 0x02004cd8)
 *   pool +0x60 -> constant 0x04001008 (image word 0x04001008)
 *   pool +0x64 -> constant 0x0400000a (image word 0x0400000a)
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fb958; the literal pool and
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

extern u8 native_data_0220def8[];
extern void native_fn_021f27d4(void);
extern u8 native_data_0220df10[];
extern u8 native_data_0220df28[];


asm u32 native_ov006_021fb958 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =native_data_0220def8
    ldr r1, =0x02004fd8
    bl native_fn_021f27d4
    ldr r0, =native_data_0220df10
    ldr r1, =0x020048a0
    bl native_fn_021f27d4
    ldr r0, =native_data_0220df28
    ldr r1, =0x02004cd8
    bl native_fn_021f27d4
    ldr r3, =0x04001008
    mov r0, #0x3
    ldrh r2, [r3, #0]
    mov r1, #0x3
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0]
    ldrh r2, [r3, #0x2]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0x2]
    ldr r3, =0x0400000a
    ldrh r2, [r3, #0]
    bic r2, r0
    orr r2, r1
    strh r2, [r3, #0]
    ldrh r2, [r3, #0x2]
    bic r2, r0
    add r0, r2, #0x0
    orr r0, r1
    strh r0, [r3, #0x2]
    pop {r3, pc}
    mov r8, r8
}
