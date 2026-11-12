/* ov000 row 0x021ed63c: 128 bytes.
 *
 * What it does: 30 instructions; 5 call(s) to 0x02065da0, 0x02065d88, 0x02063144, +2 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x78 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x7c -> constant 0x02236bc4 (image word 0x02236bc4)
 *   branch +0x28 -> +0x50
 *   branch +0x5c -> +0x68
 *   test +0x24 cmp r0, #0
 *   test +0x48 cmp r5, #1
 *   test +0x58 cmp r0, #0
 *   test +0x68 cmp r5, r4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ed63c; the literal pool and
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

extern void native_fn_02065da0(void);
extern void native_fn_02065d88(void);
extern void native_fn_02063144(void);
extern void native_fn_02063da8(void);


asm u32 native_ov000_021ed63c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    bl native_fn_02065da0
    mov r5, r0
    mov r0, r4
    bl native_fn_02065d88
    ldr r4, [r0, #0x4]
    mov r0, #28
    bl native_fn_02063144
    cmp r0, #0
    ble ov000_021ed63c_L50
    mov r0, #20
    mul r1, r5, r0
    ldr r2, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #5
    sub r5, r5, r3
    cmp r5, #1
    movle r5, #1
ov000_021ed63c_L50:
    ldr r0, =0x02236bc4
    ldrb r0, [r0]
    cmp r0, #0
    bne ov000_021ed63c_L68
    bl native_fn_02063da8
    sub r5, r5, r0
ov000_021ed63c_L68:
    cmp r5, r4
    movle r5, r4
    mov r0, r5
    ldmia sp!, {r3, r4, r5, pc}
}
