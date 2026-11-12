/* ov006 row 0x021f7d48: 56 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> constant 0x0221c0cc (image word 0x0221c0cc)
 *   pool +0x30 -> constant 0x00000438 (image word 0x00000438)
 *   pool +0x34 -> native_fn_021f7bf8+1 (image word 0x021f7bf9)
 *   branch +0x1c -> +0x28
 *   test +0x1a cmp r1, r0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f7d48; the literal pool and
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

extern void native_fn_021f7b9c(void);
extern void native_fn_021f7bc0(void);
extern void native_fn_021f7bc4(void);
extern void native_fn_021ff718(void);
extern void native_fn_021f7bf8(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f7d48 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f7b9c
    bl native_fn_021f7bc0
    bl native_fn_021f7bc4
    ldr r0, =0x0221c0cc
    ldrh r1, [r0, #0x2]
    add r1, r1, #0x1
    strh r1, [r0, #0x2]
    ldrh r1, [r0, #0x2]
    ldr r0, =0x00000438
    cmp r1, r0
    blo ov006_021f7d48_L28
    bl native_fn_021ff718
    ldr r0, =native_fn_021f7bf8+1
    bl native_fn_021f52cc
ov006_021f7d48_L28:
    pop {r3, pc}
    mov r8, r8
}
