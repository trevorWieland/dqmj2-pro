/* ov006 row 0x02203058: 48 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> constant 0x0221c178 (image word 0x0221c178)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02203058; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 13 of 48 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02202c5c(void);
extern void native_fn_02202dc0(void);
extern void native_fn_02202ff0(void);


asm u32 native_ov006_02203058 (register u32 a0)
{
    push {r4, r5, r6, lr}
    add r5, r0, #0x0
    add r4, r1, #0x0
    ldr r1, =0x0221c178
    lsl r3, r5, #0x2
    ldr r3, [r1, r3]
    lsl r1, r4, #0x3
    ldrh r1, [r3, r1]
    bl native_fn_02202c5c
    mov r1, #0x0
    add r6, r0, #0x0
    bl native_fn_02202dc0
    add r2, r0, #0x0
    add r0, r5, #0x0
    add r1, r4, #0x0
    bl native_fn_02202ff0
    add r0, r6, #0x0
    pop {r4, r5, r6, pc}
    mov r8, r8
}
