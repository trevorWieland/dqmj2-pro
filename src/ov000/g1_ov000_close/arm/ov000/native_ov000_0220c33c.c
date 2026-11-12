/* ov000 row 0x0220c33c: 172 bytes.
 *
 * What it does: 43 instructions; 3 call(s) to 0x0220a2a4, 0x0220c164, 0x02209c68; loops (back edge at +0x1c); returns through pop {r4, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x3c
 *   branch +0x88 -> +0x98
 *   test +0x0c cmp r1, #0
 *   test +0x3c cmp r1, #10
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220c33c; the literal pool and
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

extern void native_fn_0220a2a4(void);
extern void native_fn_0220c164(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220c33c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r4, r0
    ldrb r1, [r4, #0x279]
    cmp r1, #0
    bne ov000_0220c33c_L3c
    mov r1, #0
    mov r2, r1
    bl native_fn_0220a2a4
    mov r0, r4
    bl native_fn_0220c164
    mov r0, #1
    strb r0, [r4, #0x2c1]
    mov r0, #10
    strb r0, [r4, #0x279]
    ldmia sp!, {r4, pc}
ov000_0220c33c_L3c:
    cmp r1, #10
    ldmneia sp!, {r4, pc}
    ldr r2, [r4, #0x294]
    ldr r1, [r4, #0x74]
    ldr lr, [r4, #0x290]
    sub r2, r2, r1
    smull r1, r3, r2, r2
    ldr r2, [r4, #0x70]
    ldr r12, [r4, #0x298]
    sub lr, lr, r2
    ldr r2, [r4, #0x78]
    smlal r1, r3, lr, lr
    sub r2, r12, r2
    smlal r1, r3, r2, r2
    mov r1, r1, lsr #12
    orr r1, r1, r3, lsl #20
    subs r1, r1, #4096
    mov r2, #0
    rscs r1, r2, r3, asr #12
    bge ov000_0220c33c_L98
    mov r1, #6
    strb r2, [r4, #0x2c1]
    bl native_fn_02209c68
ov000_0220c33c_L98:
    ldr r0, [r4, #0x74]
    sub r0, r0, #51
    sub r0, r0, #2816
    str r0, [r4, #0x74]
    ldmia sp!, {r4, pc}
}
