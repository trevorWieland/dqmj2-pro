/* ov006 row 0x02202c1c: 64 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x38 -> native_data_0221c174 (image word 0x0221c174)
 *   pool +0x3c -> native_data2_0221c174 (image word 0x0221c174)
 *   back edge +0x2e -> +0x0c
 *   test +0x2c cmp r4, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202c1c; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 64 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0221c174[];
extern void native_fn_02204254(void);
extern void native_fn_022030c8(void);
extern u8 native_data2_0221c174[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_02202c1c (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r4, #0x0
    mov r7, #0x8a
    ldr r6, =native_data_0221c174
    add r5, r4, #0x0
    lsl r7, r7, #0x2
ov006_02202c1c_Lc:
    ldr r0, [r6, #0]
    add r1, r0, r5
    mov r0, #0x22
    lsl r0, r0, #0x4
    ldr r0, [r1, r0]
    bl native_fn_02204254
    ldr r0, [r6, #0]
    add r1, r0, r5
    mov r0, #0x89
    lsl r0, r0, #0x2
    ldr r0, [r1, r0]
    bl native_fn_022030c8
    add r4, r4, #0x1
    add r5, r5, r7
    cmp r4, #0x2
    blt ov006_02202c1c_Lc
    ldr r0, =native_data2_0221c174
    bl native_fn_02203c20
    pop {r3, r4, r5, r6, r7, pc}
}
