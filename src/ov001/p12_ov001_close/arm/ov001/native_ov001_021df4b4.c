/* ov001 row 0x021df4b4: 164 bytes.
 *
 * What it does: 40 instructions; 6 call(s) to 0x02216834, 0x02216898, 0x02044424, +3 more; loops (back edge at +0x2c); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 6 calls (40 instructions, 6 calls, 7 branches, 3 back edges, 1 literal slot).
 *
 *   pool +0xa0 -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x0c -> +0x98
 *   branch +0x24 -> +0x50
 *   branch +0x34 -> +0x50
 *   branch +0x4c -> +0x98
 *   branch +0x58 -> +0x6c
 *   branch +0x68 -> +0x98
 *   branch +0x88 -> +0x98
 *   test +0x08 cmp r0, #0
 *   test +0x20 cmp r0, #1
 *   test +0x30 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x78 cmp r0, #0
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021df4b4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02216834(void);
extern void native_fn_02216898(void);
extern void native_fn_02044424(void);
extern void native_fn_021e66f8(void);
extern void native_fn_021dda80(void);
extern void native_fn_021db8d0(void);


asm u32 native_ov001_021df4b4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl native_fn_02216834
    cmp r0, #0
    beq ov001_021df4b4_L98
    bl native_fn_02216898
    ldr r0, =0x022388ec
    ldr r0, [r0, #0x48]
    ldrb r0, [r0, #0x31e]
    cmp r0, #1
    bne ov001_021df4b4_L50
    mov r0, #128
    bl native_fn_02044424
    cmp r0, #0
    beq ov001_021df4b4_L50
    mov r0, #4
    bl native_fn_021e66f8
    ldr r0, =0x022388ec
    mov r1, #54
    strb r1, [r0, #0x8]
    b ov001_021df4b4_L98
ov001_021df4b4_L50:
    bl native_fn_021dda80
    cmp r0, #0
    beq ov001_021df4b4_L6c
    ldr r0, =0x022388ec
    mov r1, #54
    strb r1, [r0, #0x8]
    b ov001_021df4b4_L98
ov001_021df4b4_L6c:
    ldr r0, =0x022388ec
    ldr r0, [r0, #0x48]
    bl native_fn_021db8d0
    cmp r0, #0
    ldreq r0, =0x022388ec
    moveq r1, #24
    streqb r1, [r0, #0x8]
    beq ov001_021df4b4_L98
    ldr r0, =0x022388ec
    mov r1, #15
    strb r1, [r0, #0x8]
ov001_021df4b4_L98:
    mov r0, #0
    ldmia sp!, {r3, pc}
}
