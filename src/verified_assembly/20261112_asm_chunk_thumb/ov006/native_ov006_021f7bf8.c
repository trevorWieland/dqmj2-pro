/* ov006 row 0x021f7bf8: 44 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x24 -> constant 0x0221c0cc (image word 0x0221c0cc)
 *   pool +0x28 -> native_fn_021f7c24+1 (image word 0x021f7c25)
 *   branch +0x0c -> +0x14
 *   test +0x0a cmp r1, #0x0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f7bf8; the literal pool and
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

extern void native_fn_021f23f4(void);
extern void native_fn_0220498c(void);
extern void native_fn_022032e0(void);
extern void native_fn_021f7c24(void);
extern void native_fn_021f52cc(void);


asm u32 native_ov006_021f7bf8 (register u32 a0)
{
    push {r3, lr}
    bl native_fn_021f23f4
    ldr r0, =0x0221c0cc
    ldr r1, [r0, #0x4]
    cmp r1, #0x0
    beq ov006_021f7bf8_L14
    mov r0, #0x1
    bl native_fn_0220498c
ov006_021f7bf8_L14:
    mov r0, #0x8
    bl native_fn_022032e0
    ldr r0, =native_fn_021f7c24+1
    bl native_fn_021f52cc
    pop {r3, pc}
    mov r8, r8
}
