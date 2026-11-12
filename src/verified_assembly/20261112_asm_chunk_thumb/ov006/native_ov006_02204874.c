/* ov006 row 0x02204874: 52 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> native_data_0221c1e8 (image word 0x0221c1e8)
 *   pool +0x30 -> native_data2_0221c1e8 (image word 0x0221c1e8)
 *   back edge +0x20 -> +0x08
 *   test +0x1e cmp r4, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02204874; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 52 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0221c1e8[];
extern void native_fn_02204254(void);
extern void native_fn_022030c8(void);
extern u8 native_data2_0221c1e8[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_02204874 (register u32 a0)
{
    push {r4, r5, r6, lr}
    mov r4, #0x0
    ldr r6, =native_data_0221c1e8
    add r5, r4, #0x0
ov006_02204874_L8:
    ldr r0, [r6, #0]
    add r0, r0, r5
    ldr r0, [r0, #0x8]
    bl native_fn_02204254
    ldr r0, [r6, #0]
    ldr r0, [r0, r5]
    bl native_fn_022030c8
    add r4, r4, #0x1
    add r5, #0x40
    cmp r4, #0x2
    blt ov006_02204874_L8
    ldr r0, =native_data2_0221c1e8
    bl native_fn_02203c20
    pop {r4, r5, r6, pc}
    mov r8, r8
}
