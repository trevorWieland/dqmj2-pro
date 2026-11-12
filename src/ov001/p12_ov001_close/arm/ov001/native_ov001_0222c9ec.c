/* ov001 row 0x0222c9ec: 220 bytes.
 *
 * What it does: 55 instructions; 7 call(s) to 0x02008e0c, 0x02008e0c, 0x02008e0c, +4 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 7 calls (55 instructions, 7 calls, 1 branch, 7 back edges, 0 literal slots).
 *
 *   branch +0x18 -> +0x2c
 *   test +0x14 cmpne r0, #0
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222c9ec; the literal pool and
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

extern void native_fn_02008e0c(void);
extern void native_fn_0207b1c4(void);
extern void native_fn_0207c078(void);


asm u32 native_ov001_0222c9ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    movs r5, r1
    mov r6, r0
    ldrnesh r0, [r5, #24]
    mov r4, r2
    cmpne r0, #0
    bne ov001_0222c9ec_L2c
    mvn r0, #0
    strh r0, [r6, #46]
    str r0, [r6]
    ldmia sp!, {r4, r5, r6, pc}
ov001_0222c9ec_L2c:
    mov r0, r5
    add r1, r6, #182
    mov r2, #20
    bl native_fn_02008e0c
    ldrsh r2, [r5, #24]
    add r0, r5, #122
    add r1, r6, #214
    str r2, [r6]
    ldrsh r3, [r5, #24]
    mov r2, #10
    strh r3, [r6, #46]
    ldrb r3, [r5, #0x1a]
    strb r3, [r6, #0x30]
    ldr r3, [r5, #0x14]
    str r3, [r6, #0x4]
    ldrb r3, [r5, #0x1b]
    strb r3, [r6, #0xb1]
    ldrb r3, [r5, #0x1e]
    strb r3, [r6, #0xb2]
    ldrb r3, [r5, #0x1c]
    strb r3, [r6, #0xaf]
    bl native_fn_02008e0c
    add r0, r5, #64
    add r1, r6, #224
    mov r2, #58
    bl native_fn_02008e0c
    add r0, r5, #32
    add r1, r6, #284
    mov r2, #32
    bl native_fn_02008e0c
    mov r0, r4
    add r1, r6, #74
    mov r2, #64
    bl native_fn_02008e0c
    add r0, r5, #122
    add r1, r6, #74
    add r2, r6, #12
    bl native_fn_0207b1c4
    ldrsh r0, [r6, #46]
    ldrb r1, [r6, #0x30]
    add r2, r6, #74
    add r3, r6, #138
    bl native_fn_0207c078
    ldmia sp!, {r4, r5, r6, pc}
}
