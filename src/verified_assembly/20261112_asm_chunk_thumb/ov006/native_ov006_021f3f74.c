/* ov006 row 0x021f3f74: 160 bytes.
 *
 * What it does: Writes 2 blocks of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x98 -> native_data5_0221c05c (image word 0x0221c05c)
 *   pool +0x9c -> native_data6_0221c05c (image word 0x0221c05c)
 *   branch +0x20 -> +0x32
 *   back edge +0x38 -> +0x12
 *   back edge +0x40 -> +0x0e
 *   back edge +0x5a -> +0x48
 *   back edge +0x74 -> +0x62
 *   back edge +0x8c -> +0x7c
 *   test +0x1e cmp r7, #0x0
 *   test +0x36 cmp r4, #0x4
 *   test +0x3e cmp r7, #0x3
 *   test +0x58 cmp r5, #0x2
 *   test +0x72 cmp r5, #0x4
 *   test +0x8a cmp r5, #0x2f
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f3f74; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 13 of 160 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02204974(void);
extern u8 native_data5_0221c05c[];
extern void native_fn_022034bc(void);
extern void native_fn_02202d64(void);
extern void native_fn_022043a4(void);
extern u8 native_data6_0221c05c[];
extern void native_fn_02203c20(void);


asm u32 native_ov006_021f3f74 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    add r1, r0, #0x0
    mov r0, #0x0
    bl native_fn_02204974
    mov r7, #0x0
    add r6, r7, #0x0
ov006_021f3f74_Le:
    mov r4, #0x0
    add r5, r4, #0x0
ov006_021f3f74_L12:
    ldr r0, =native_data5_0221c05c
    ldr r0, [r0, #0]
    add r0, r6, r0
    ldr r0, [r5, r0]
    bl native_fn_022034bc
    cmp r7, #0x0
    bne ov006_021f3f74_L32
    ldr r0, =native_data5_0221c05c
    ldr r0, [r0, #0]
    add r1, r0, r5
    mov r0, #0x41
    lsl r0, r0, #0x2
    ldr r0, [r1, r0]
    bl native_fn_02202d64
ov006_021f3f74_L32:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x4
    blt ov006_021f3f74_L12
    add r7, r7, #0x1
    add r6, #0x10
    cmp r7, #0x3
    blt ov006_021f3f74_Le
    mov r5, #0x0
    ldr r6, =native_data5_0221c05c
    add r4, r5, #0x0
ov006_021f3f74_L48:
    ldr r0, [r6, #0]
    add r0, r0, r4
    add r0, #0xfc
    ldr r0, [r0, #0]
    bl native_fn_02202d64
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2
    blt ov006_021f3f74_L48
    mov r5, #0x0
    ldr r6, =native_data5_0221c05c
    add r4, r5, #0x0
ov006_021f3f74_L62:
    ldr r0, [r6, #0]
    add r0, r0, r4
    add r0, #0xec
    ldr r0, [r0, #0]
    bl native_fn_022043a4
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x4
    blt ov006_021f3f74_L62
    mov r5, #0x0
    ldr r6, =native_data5_0221c05c
    add r4, r5, #0x0
ov006_021f3f74_L7c:
    ldr r0, [r6, #0]
    add r0, r0, r4
    ldr r0, [r0, #0x30]
    bl native_fn_022043a4
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x2f
    blt ov006_021f3f74_L7c
    ldr r0, =native_data6_0221c05c
    bl native_fn_02203c20
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
