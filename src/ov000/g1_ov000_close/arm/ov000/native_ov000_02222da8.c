/* ov000 row 0x02222da8: 212 bytes.
 *
 * What it does: 49 instructions; 7 call(s) to 0x02041800, 0x0201d444, 0x0201d444, +4 more; loops (back edge at +0x08); returns through pop {r3, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc4 -> constant 0x02246574 (image word 0x02246574)
 *   pool +0xc8 -> native_data_0222fcb4 (image word 0x0222fcb4)
 *   pool +0xcc -> native_data_0222fcc8 (image word 0x0222fcc8)
 *   pool +0xd0 -> native_data_0222fcdc (image word 0x0222fcdc)
 *   branch +0x28 -> +0x40
 *   branch +0x30 -> +0x50
 *   branch +0x38 -> +0x60
 *   branch +0x3c -> +0x6c
 *   branch +0x4c -> +0x6c
 *   branch +0x5c -> +0x6c
 *   test +0x0c cmp r0, #1
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmp r0, #1
 *   test +0x34 cmp r0, #2
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02222da8; the literal pool and
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

extern void native_fn_02041800(void);
extern u8 native_data_0222fcb4[];
extern void native_fn_0201d444(void);
extern u8 native_data_0222fcc8[];
extern u8 native_data_0222fcdc[];
extern void native_fn_02223390(void);
extern void native_fn_020414b0(void);
extern void native_fn_02041510(void);


asm u32 native_ov000_02222da8 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #32
    bl native_fn_02041800
    cmp r0, #1
    addeq sp, sp, #32
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    ldr r0, =0x02246574
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    beq ov000_02222da8_L40
    cmp r0, #1
    beq ov000_02222da8_L50
    cmp r0, #2
    beq ov000_02222da8_L60
    b ov000_02222da8_L6c
ov000_02222da8_L40:
    ldr r1, =native_data_0222fcb4
    add r0, sp, #0
    bl native_fn_0201d444
    b ov000_02222da8_L6c
ov000_02222da8_L50:
    ldr r1, =native_data_0222fcc8
    add r0, sp, #0
    bl native_fn_0201d444
    b ov000_02222da8_L6c
ov000_02222da8_L60:
    ldr r1, =native_data_0222fcdc
    add r0, sp, #0
    bl native_fn_0201d444
ov000_02222da8_L6c:
    add r0, sp, #0
    bl native_fn_02223390
    mov r0, #63
    bl native_fn_020414b0
    mov r0, #0
    mov r1, #2
    mov r2, #10
    bl native_fn_02041510
    ldr r0, =0x02246574
    mov r1, #6
    strb r1, [r0]
    mov r2, #67108864
    ldr r1, [r2]
    mov r0, #0
    bic r1, r1, #7936
    orr r1, r1, #2048
    str r1, [r2]
    ldr r1, [r2]
    bic r1, r1, #57344
    str r1, [r2]
    add sp, sp, #32
    ldmia sp!, {r3, pc}
}
