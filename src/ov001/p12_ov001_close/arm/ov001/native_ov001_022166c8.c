/* ov001 row 0x022166c8: 84 bytes.
 *
 * What it does: 19 instructions; 2 call(s) to 0x021f1294, 0x0220f9a4; loops (back edge at +0x0c); returns through pop {r3, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (19 instructions, 2 calls, 0 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x4c -> native_data_02242be8 (image word 0x02242be8)
 *   pool +0x50 -> native_data2_02242be8 (image word 0x02242be8)
 *   test +0x2c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022166c8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021f1294(void);
extern u8 native_data_02242be8[];
extern u8 native_data2_02242be8[];
extern void native_fn_0220f9a4(void);


asm u32 native_ov001_022166c8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r0, #16
    mov r1, #2
    bl native_fn_021f1294
    ldr r0, =native_data_02242be8
    ldr r2, =native_data2_02242be8
    ldr r3, [r0, #0x8]
    ldrh r1, [r0, #4]
    ldr r0, [r3, #0x1e8]
    add r0, r0, #70
    bl native_fn_0220f9a4
    cmp r0, #0
    ldrne r0, =native_data_02242be8
    movne r1, #2
    ldreq r0, =native_data_02242be8
    moveq r1, #1
    strb r1, [r0, #0x1]
    mov r0, #1
    ldmia sp!, {r3, pc}
}
