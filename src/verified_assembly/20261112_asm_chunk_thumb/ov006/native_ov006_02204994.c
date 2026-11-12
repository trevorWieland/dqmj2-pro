/* ov006 row 0x02204994: 48 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> constant 0x0221c1e8 (image word 0x0221c1e8)
 *   branch +0x0a -> +0x14
 *   test +0x08 cmp r0, #0x0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204994; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 12 of 48 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02203c20(void);
extern void native_fn_02204268(void);
extern void native_fn_022030dc(void);


asm u32 native_ov006_02204994 (register u32 a0)
{
    push {r3, r4, r5, lr}
    add r4, r1, #0x0
    add r5, r0, #0x0
    ldrb r0, [r4, #0x11]
    cmp r0, #0x0
    beq ov006_02204994_L14
    add r0, r4, #0x0
    add r0, #0xc
    bl native_fn_02203c20
ov006_02204994_L14:
    add r0, r4, #0x0
    bl native_fn_02204268
    ldr r0, =0x0221c1e8
    ldr r1, [r0, #0]
    lsl r0, r5, #0x6
    ldr r0, [r1, r0]
    add r1, r4, #0x0
    bl native_fn_022030dc
    pop {r3, r4, r5, pc}
    mov r8, r8
}
