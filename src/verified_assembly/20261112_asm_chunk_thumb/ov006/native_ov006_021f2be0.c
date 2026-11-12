/* ov006 row 0x021f2be0: 44 bytes.
 *
 * What it does: Writes 2 blocks of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24 -> native_data2_0221c058 (image word 0x0221c058)
 *   pool +0x28 -> native_data3_0221c058 (image word 0x0221c058)
 *   branch +0x08 -> +0x22
 *   test +0x06 cmp r1, #0x0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f2be0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 44 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data2_0221c058[];
extern void native_fn_0220498c(void);
extern void native_fn_022043a4(void);
extern u8 native_data3_0221c058[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f2be0 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =native_data2_0221c058
    ldr r1, [r0, #0]
    cmp r1, #0x0
    beq ov006_021f2be0_L22
    ldr r1, [r1, #0x4]
    mov r0, #0x0
    bl native_fn_0220498c
    ldr r0, =native_data2_0221c058
    ldr r0, [r0, #0]
    ldr r0, [r0, #0]
    bl native_fn_022043a4
    ldr r0, =native_data3_0221c058
    bl native_fn_02203c20
ov006_021f2be0_L22:
    pop {r3, pc}
}
