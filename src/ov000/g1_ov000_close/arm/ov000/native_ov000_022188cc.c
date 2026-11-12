/* ov000 row 0x022188cc: 148 bytes.
 *
 * What it does: 33 instructions; 4 call(s) to 0x021df3bc, 0x0201d444, 0x0202a8e0, +1 more; loops (back edge at +0x0c); returns through pop {r4, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x84 -> native_data_0222fa10 (image word 0x0222fa10)
 *   pool +0x88 -> constant 0x02245e54 (image word 0x02245e54)
 *   pool +0x8c -> native_data_0222faac (image word 0x0222faac)
 *   pool +0x90 -> native_data_0222fa08 (image word 0x0222fa08)
 *   test +0x20 cmp r3, #255
 *   test +0x4c cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022188cc; the literal pool and
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

extern void native_fn_021df3bc(void);
extern u8 native_data_0222fa10[];
extern u8 native_data_0222faac[];
extern void native_fn_0201d444(void);
extern void native_fn_0202a8e0(void);
extern void native_fn_0203cc2c(void);
extern u8 native_data_0222fa08[];


asm u32 native_ov000_022188cc (register u32 a0)
{
    stmdb sp!, {r4, lr}
    sub sp, sp, #16
    mov r4, r0
    bl native_fn_021df3bc
    ldrh r1, [r0]
    ldrb r3, [r0, #0x3]
    ldr r0, =native_data_0222fa10
    mov r1, r1, lsl #16
    cmp r3, #255
    ldrb r2, [r0, r1, lsr #27]
    ldreq r0, =0x02245e54
    addeq sp, sp, #16
    ldreq r0, [r0, #0x34]
    ldmeqia sp!, {r4, pc}
    ldr r1, =native_data_0222faac
    add r0, sp, #0
    bl native_fn_0201d444
    add r0, sp, #0
    bl native_fn_0202a8e0
    cmp r0, #0
    ldreq r0, =0x02245e54
    addeq sp, sp, #16
    ldreq r0, [r0, #0x34]
    ldmeqia sp!, {r4, pc}
    add r0, sp, #0
    mov r1, #2
    bl native_fn_0203cc2c
    ldr r2, =0x02245e54
    ldr r1, =native_data_0222fa08
    str r0, [r2, #0x34]
    strb r4, [r1, #0x1]
    add sp, sp, #16
    ldmia sp!, {r4, pc}
}
