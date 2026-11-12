/* ov006 row 0x0220167c: 56 bytes.
 *
 * What it does: Writes one block of 3 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x30 -> constant 0x0221c164 (image word 0x0221c164)
 *   pool +0x34 -> native_data_0220e760 (image word 0x0220e760)
 *   branch +0x06 -> +0x12
 *   branch +0x18 -> +0x2e
 *   branch +0x20 -> +0x2a
 *   test +0x04 cmp r0, #0x0
 *   test +0x16 cmp r0, #0x0
 *   test +0x1e cmp r2, #0x0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x0220167c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 56 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_022012c0(void);
extern void native_fn_02201cf4(void);
extern void native_fn_022016b4(void);
extern u8 native_data_0220e760[];


asm u32 native_ov006_0220167c (register u32 a0)
{
    push {r3, lr}
    ldrh r0, [r0, #0x2]
    cmp r0, #0x0
    beq ov006_0220167c_L12
    bl native_fn_022012c0
    bl native_fn_02201cf4
    pop {r3, pc}
ov006_0220167c_L12:
    bl native_fn_022016b4
    cmp r0, #0x0
    bne ov006_0220167c_L2e
    ldr r0, =0x0221c164
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq ov006_0220167c_L2a
    mov r0, #0x2
    ldr r1, =native_data_0220e760
    lsl r0, r0, #0x1a
    blx r2
ov006_0220167c_L2a:
    bl native_fn_02201cf4
ov006_0220167c_L2e:
    pop {r3, pc}
}
