/* ov006 row 0x02202d64: 92 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x54 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   pool +0x58 -> constant 0x0221c174 (image word 0x0221c174)
 *   branch +0x0e -> +0x28
 *   back edge +0x26 -> +0x16
 *   branch +0x3a -> +0x3e
 *   test +0x0c cmp r2, #0x0
 *   test +0x24 cmp r1, r6
 *   test +0x38 cmp r5, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202d64; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 16 of 92 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02204268(void);
extern void native_fn_022030dc(void);


asm u32 native_ov006_02202d64 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r5, r0, #0x0
    ldrb r2, [r5, #0xc]
    mov r4, #0x0
    add r1, r4, #0x0
    ldr r0, [r5, #0x8]
    cmp r2, #0x0
    ble ov006_02202d64_L28
    mov r3, #0x2
    ldr r2, =0xc1fffcff
    lsl r3, r3, #0x8
ov006_02202d64_L16:
    ldr r6, [r0, #0]
    add r1, r1, #0x1
    and r6, r2
    orr r6, r3
    str r6, [r0, #0]
    ldrb r6, [r5, #0xc]
    add r0, #0x8
    cmp r1, r6
    blt ov006_02202d64_L16
ov006_02202d64_L28:
    add r0, r5, #0x0
    bl native_fn_02204268
    ldr r0, =0x0221c174
    ldr r2, [r0, #0]
    mov r0, #0x8a
    lsl r0, r0, #0x2
    add r0, r2, r0
    cmp r5, r0
    blo ov006_02202d64_L3e
    mov r4, #0x1
ov006_02202d64_L3e:
    mov r0, #0x8a
    lsl r0, r0, #0x2
    add r1, r4, #0x0
    mul r1, r0
    add r1, r2, r1
    sub r0, r0, #0x4
    ldr r0, [r1, r0]
    add r1, r5, #0x0
    bl native_fn_022030dc
    pop {r4, r5, r6, pc}
}
