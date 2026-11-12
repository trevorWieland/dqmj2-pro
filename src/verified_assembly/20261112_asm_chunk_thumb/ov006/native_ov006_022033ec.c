/* ov006 row 0x022033ec: 64 bytes.
 *
 * What it does: Writes 2 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x34 -> native_data2_0221c184 (image word 0x0221c184)
 *   pool +0x38 -> constant 0x00000674 (image word 0x00000674)
 *   pool +0x3c -> native_data3_0221c184 (image word 0x0221c184)
 *   back edge +0x1a -> +0x0a
 *   test +0x18 cmp r4, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022033ec; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 64 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0221c184[];
extern void native_fn_02202b24(void);
extern void native_fn_022030c8(void);
extern u8 native_data3_0221c184[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_022033ec (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r4, #0x0
    ldr r6, =native_data2_0221c184
    ldr r7, =0x00000674
    add r5, r4, #0x0
ov006_022033ec_La:
    ldr r0, [r6, #0]
    add r0, r0, r5
    ldr r0, [r0, r7]
    bl native_fn_02202b24
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x2
    blt ov006_022033ec_La
    ldr r0, =native_data2_0221c184
    ldr r1, [r0, #0]
    mov r0, #0x67
    lsl r0, r0, #0x4
    ldr r0, [r1, r0]
    bl native_fn_022030c8
    ldr r0, =native_data3_0221c184
    bl native_fn_02203c20
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
