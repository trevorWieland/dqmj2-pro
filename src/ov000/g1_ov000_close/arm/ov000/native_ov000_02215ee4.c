/* ov000 row 0x02215ee4: 148 bytes.
 *
 * What it does: 34 instructions; 9 call(s) to 0x02215ee4, 0x020620a0, 0x02214fc8, +6 more; loops (back edge at +0x24); returns through pop {r4, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x88 -> constant 0x022459b4 (image word 0x022459b4)
 *   pool +0x8c -> native_data_0222f964 (image word 0x0222f964)
 *   pool +0x90 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x20 -> +0x30
 *   back edge +0x24 -> +0x00
 *   branch +0x2c -> +0x80
 *   branch +0x34 -> +0x68
 *   branch +0x40 -> +0x5c
 *   branch +0x64 -> +0x80
 *   test +0x1c cmp r0, #2
 *   test +0x30 cmp r0, #3
 *   test +0x3c cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02215ee4; the literal pool and
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

extern u8 native_data_0222f964[];
extern void native_fn_020620a0(void);
extern void native_fn_02214fc8(void);
extern void native_fn_02062074(void);
extern void native_fn_020406a8(void);
extern void native_fn_02214fe0(void);
extern void native_fn_02217260(void);
extern void native_fn_020851d4(void);
extern void native_fn_02085200(void);


asm u32 native_ov000_02215ee4 (register u32 a0)
{
ov000_02215ee4_L0:
    stmdb sp!, {r4, lr}
    ldr r0, =0x022459b4
    ldr r1, =native_data_0222f964
    ldrb r0, [r0, #0x494]
    mov r4, #1
    ldr r0, [r1, r0, lsl #2]
    blx r0
    cmp r0, #2
    bne ov000_02215ee4_L30
    bl ov000_02215ee4_L0
    mov r4, r0
    b ov000_02215ee4_L80
ov000_02215ee4_L30:
    cmp r0, #3
    bne ov000_02215ee4_L68
    bl native_fn_020620a0
    cmp r0, #0
    beq ov000_02215ee4_L5c
    mov r0, #2
    bl native_fn_02214fc8
    mov r0, #0
    bl native_fn_02062074
    mov r0, #0
    bl native_fn_020406a8
ov000_02215ee4_L5c:
    bl native_fn_02214fe0
    mov r4, r0
    b ov000_02215ee4_L80
ov000_02215ee4_L68:
    bl native_fn_02217260
    bl native_fn_020851d4
    bl native_fn_02085200
    ldr r0, =0x02101ae8
    mov r1, r4
    str r1, [r0, #0xc84]
ov000_02215ee4_L80:
    mov r0, r4
    ldmia sp!, {r4, pc}
}
