/* ov000 row 0x02218b74: 176 bytes.
 *
 * What it does: 43 instructions; 7 call(s) to 0x021df1f0, 0x021df3bc, 0x02215048, +4 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xac -> native_data_0222fa10 (image word 0x0222fa10)
 *   branch +0x48 -> +0x94
 *   branch +0x50 -> +0x68
 *   branch +0x60 -> +0x94
 *   branch +0x64 -> +0x74
 *   branch +0x70 -> +0x94
 *   branch +0x88 -> +0x94
 *   back edge +0xa4 -> +0x30
 *   test +0x24 cmpne r6, #16
 *   test +0x44 cmp r0, #0
 *   test +0x4c cmp r9, #0
 *   test +0x5c cmp r1, r0
 *   test +0x6c cmp r0, #1
 *   test +0x84 cmp r1, r0
 *   test +0xa0 cmp r5, #768
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218b74; the literal pool and
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

extern void native_fn_021df1f0(void);
extern void native_fn_021df3bc(void);
extern u8 native_data_0222fa10[];
extern void native_fn_02215048(void);
extern void native_fn_0205fb90(void);
extern void native_fn_02218c24(void);


asm u32 native_ov000_02218b74 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    bl native_fn_021df1f0
    mov r8, r0
    bl native_fn_021df3bc
    ldrh r0, [r0]
    ldr r4, =native_data_0222fa10
    mov r5, #0
    mov r0, r0, lsl #16
    movs r6, r0, lsr #27
    cmpne r6, #16
    moveq r9, #1
    movne r9, #0
ov000_02218b74_L30:
    mov r0, r5
    bl native_fn_02215048
    mov r7, r0
    mov r0, r5
    bl native_fn_0205fb90
    cmp r0, #0
    beq ov000_02218b74_L94
    cmp r9, #0
    bne ov000_02218b74_L68
    ldrb r1, [r7]
    ldrsb r0, [r4, r6]
    cmp r1, r0
    bne ov000_02218b74_L94
    b ov000_02218b74_L74
ov000_02218b74_L68:
    ldrb r0, [r7]
    cmp r0, #1
    bne ov000_02218b74_L94
ov000_02218b74_L74:
    mov r0, r8
    bl native_fn_021df3bc
    ldrb r1, [r7, #0x1]
    ldrb r0, [r0, #0x3]
    cmp r1, r0
    bne ov000_02218b74_L94
    mov r0, r5
    bl native_fn_02218c24
ov000_02218b74_L94:
    add r0, r5, #1
    mov r0, r0, lsl #16
    mov r5, r0, lsr #16
    cmp r5, #768
    blo ov000_02218b74_L30
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
