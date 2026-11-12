/* ov006 row 0x021ffd50: 132 bytes.
 *
 * What it does: Writes 2 blocks of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x74 -> native_data3_0221c150 (image word 0x0221c150)
 *   pool +0x78 -> native_data_0220ba12 (image word 0x0220ba12)
 *   pool +0x7c -> constant 0x000001d6 (image word 0x000001d6)
 *   pool +0x80 -> constant 0x0221c154 (image word 0x0221c154)
 *   back edge +0x3c -> +0x24
 *   branch +0x44 -> +0x70
 *   branch +0x4a -> +0x70
 *   back edge +0x68 -> +0x5a
 *   test +0x3a cmp r6, #0x5
 *   test +0x42 cmp r1, r0
 *   test +0x48 cmp r1, r0
 *   test +0x66 cmp r5, #0x5
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ffd50; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 14 of 132 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data3_0221c150[];
extern void native_fn_02202f98(void);
extern u8 native_data_0220ba12[];
extern void native_fn_02202eb0(void);
extern void native_fn_02204974(void);
extern void native_fn_02202d64(void);
extern void native_fn_02203c20(void);


asm u32 native_ov006_021ffd50 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0xc
    str r0, [sp]
    ldr r0, =native_data3_0221c150
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r2, sp, #0x8
    ldr r0, [r0, #0]
    add r3, sp, #0x4
    bl native_fn_02202f98
    ldr r0, [sp, #0x8]
    mov r6, #0x0
    sub r0, #0x8
    ldr r4, =native_data_0220ba12
    ldr r7, =native_data3_0221c150
    str r0, [sp, #0x8]
    add r5, r6, #0x0
ov006_021ffd50_L24:
    ldr r0, [r7, #0x4]
    ldrh r3, [r4, #0x2]
    mov r1, #0x0
    ldr r0, [r0, r5]
    ldr r2, [sp, #0x8]
    mvn r1, r1
    bl native_fn_02202eb0
    add r6, r6, #0x1
    add r4, r4, #0x4
    add r5, r5, #0x4
    cmp r6, #0x5
    blt ov006_021ffd50_L24
    ldr r1, [sp, #0x8]
    ldr r0, =0x000001d6
    cmp r1, r0
    bgt ov006_021ffd50_L70
    sub r0, #0xd6
    cmp r1, r0
    blt ov006_021ffd50_L70
    ldr r1, [sp]
    mov r0, #0x0
    bl native_fn_02204974
    mov r5, #0x0
    ldr r6, =native_data3_0221c150
    add r4, r5, #0x0
ov006_021ffd50_L5a:
    ldr r0, [r6, #0x4]
    ldr r0, [r0, r4]
    bl native_fn_02202d64
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x5
    blt ov006_021ffd50_L5a
    ldr r0, =0x0221c154
    bl native_fn_02203c20
ov006_021ffd50_L70:
    add sp, #0xc
    pop {r4, r5, r6, r7, pc}
}
