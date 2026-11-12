/* ov000 row 0x0221e6cc: 188 bytes.
 *
 * What it does: 44 instructions; 10 call(s) to 0x0221db58, 0x0221de1c, 0x0221dee8, +7 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb0 -> constant 0x02246348 (image word 0x02246348)
 *   pool +0xb4 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   pool +0xb8 -> constant 0x02246318 (image word 0x02246318)
 *   branch +0x14 -> +0x90
 *   branch +0x3c -> +0x4c
 *   branch +0x48 -> +0x50
 *   back edge +0x88 -> +0x70
 *   branch +0x8c -> +0x94
 *   test +0x10 cmp r2, #10
 *   test +0x34 cmp r0, #8
 *   test +0x84 cmp r6, #22
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221e6cc; the literal pool and
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

extern void native_fn_0221db58(void);
extern void native_fn_0221de1c(void);
extern void native_fn_0221dee8(void);
extern void native_fn_0221e03c(void);
extern void native_fn_0221e368(void);
extern void native_fn_0221e480(void);
extern void native_fn_0221d824(void);
extern void native_fn_02048a44(void);
extern void native_fn_0206b35c(void);


asm u32 native_ov000_0221e6cc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r0
    ldrsb r2, [r5, #16]
    mov r4, r1
    cmp r2, #10
    beq ov000_0221e6cc_L90
    bl native_fn_0221db58
    mov r0, r5
    mov r1, r4
    bl native_fn_0221de1c
    mov r0, r5
    bl native_fn_0221dee8
    ldrsb r0, [r5, #16]
    cmp r0, #8
    mov r0, r5
    beq ov000_0221e6cc_L4c
    mov r1, r4
    bl native_fn_0221e03c
    b ov000_0221e6cc_L50
ov000_0221e6cc_L4c:
    bl native_fn_0221e368
ov000_0221e6cc_L50:
    mov r0, r5
    bl native_fn_0221e480
    mov r0, r5
    mov r1, r4
    bl native_fn_0221d824
    ldr r5, =0x02246348
    mov r6, #0
    mov r4, #1
ov000_0221e6cc_L70:
    ldr r0, [r5, r6, lsl #2]
    mov r1, r4
    add r0, r0, #8
    bl native_fn_02048a44
    add r6, r6, #1
    cmp r6, #22
    blt ov000_0221e6cc_L70
    b ov000_0221e6cc_L94
ov000_0221e6cc_L90:
    bl native_fn_0206b35c
ov000_0221e6cc_L94:
    ldr r1, =0x02101ae8
    mov r2, #1
    ldr r0, =0x02246318
    str r2, [r1, #0xc84]
    mov r1, #0
    strb r1, [r0]
    ldmia sp!, {r4, r5, r6, pc}
}
