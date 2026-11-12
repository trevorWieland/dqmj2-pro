/* ov006 row 0x021f3494: 40 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x20 -> constant 0x0221c05c (image word 0x0221c05c)
 *   pool +0x24 -> constant 0x0000011d (image word 0x0000011d)
 *   branch +0x0c -> +0x12
 *   branch +0x10 -> +0x14
 *   test +0x0a cmp r0, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3494; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 13 of 40 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021f3984(void);
extern void native_fn_021ff6d4(void);


asm u32 native_ov006_021f3494 (register u32 a0)
{
    push {r3, lr}
    ldr r0, =0x0221c05c
    ldr r1, [r0, #0]
    ldr r0, =0x0000011d
    ldrb r0, [r1, r0]
    cmp r0, #0x2
    bne ov006_021f3494_L12
    mov r0, #0x0
    b ov006_021f3494_L14
ov006_021f3494_L12:
    mov r0, #0x2
ov006_021f3494_L14:
    bl native_fn_021f3984
    mov r0, #0x1
    bl native_fn_021ff6d4
    pop {r3, pc}
}
