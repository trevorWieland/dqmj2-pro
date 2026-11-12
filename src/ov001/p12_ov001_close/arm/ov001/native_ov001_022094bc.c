/* ov001 row 0x022094bc: 312 bytes.
 *
 * What it does: 78 instructions; 6 call(s) to 0x021d8dec, 0x021d8dec, 0x021d8dec, +3 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 6 calls (78 instructions, 6 calls, 17 branches, 3 back edges, 0 literal slots).
 *
 *   branch +0x14 -> +0x28
 *   branch +0x24 -> +0x38
 *   branch +0x34 -> +0x44
 *   branch +0x48 -> +0x7c
 *   branch +0x50 -> +0x64
 *   branch +0x80 -> +0xac
 *   branch +0x88 -> +0xa4
 *   branch +0x90 -> +0xa4
 *   branch +0xb0 -> +0xd8
 *   branch +0xb4 -> +0xf8
 *   branch +0xbc -> +0x130
 *   branch +0xc4 -> +0x130
 *   branch +0xc8 -> +0x120
 *   branch +0xd0 -> +0x128
 *   branch +0xd4 -> +0x130
 *   branch +0xe4 -> +0x130
 *   branch +0xe8 -> +0x100
 *   branch +0xec -> +0x108
 *   branch +0xf0 -> +0x110
 *   branch +0xf4 -> +0x118
 *   test +0x10 cmp r5, #0
 *   test +0x20 cmp r0, #0
 *   test +0x44 cmp r6, #8
 *   test +0x4c cmp r5, #0
 *   test +0x7c cmp r6, #54
 *   test +0x84 cmp r4, #1
 *   test +0x8c cmp r4, #4
 *   test +0xac cmp r0, #205
 *   test +0xb8 cmp r0, #17
 *   test +0xc0 cmp r0, #16
 *   test +0xcc cmp r0, #17
 *   test +0xdc cmp r0, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022094bc; the literal pool and
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

extern void native_fn_021d8dec(void);


asm u32 native_ov001_022094bc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r1
    mov r6, r0
    mov r4, r2
    cmp r5, #0
    bgt ov001_022094bc_L28
    bl native_fn_021d8dec
    ldrsh r0, [r0, #10]
    cmp r0, #0
    bne ov001_022094bc_L38
ov001_022094bc_L28:
    mov r0, r6
    bl native_fn_021d8dec
    ldrsh r0, [r0, #4]
    b ov001_022094bc_L44
ov001_022094bc_L38:
    mov r0, r6
    bl native_fn_021d8dec
    ldrsh r0, [r0, #10]
ov001_022094bc_L44:
    cmp r6, #8
    bne ov001_022094bc_L7c
    cmp r5, #0
    ble ov001_022094bc_L64
    add r0, r5, #6
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L64:
    mvnge r0, #0
    ldmgeia sp!, {r4, r5, r6, pc}
    rsb r0, r5, #10
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L7c:
    cmp r6, #54
    bne ov001_022094bc_Lac
    cmp r4, #1
    blt ov001_022094bc_La4
    cmp r4, #4
    bgt ov001_022094bc_La4
    rsb r0, r4, #19
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_La4:
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_Lac:
    cmp r0, #205
    bgt ov001_022094bc_Ld8
    bge ov001_022094bc_Lf8
    cmp r0, #17
    bgt ov001_022094bc_L130
    cmp r0, #16
    blt ov001_022094bc_L130
    beq ov001_022094bc_L120
    cmp r0, #17
    beq ov001_022094bc_L128
    b ov001_022094bc_L130
ov001_022094bc_Ld8:
    sub r0, r0, #206
    cmp r0, #3
    addls pc, pc, r0, lsl #2
    b ov001_022094bc_L130
    b ov001_022094bc_L100
    b ov001_022094bc_L108
    b ov001_022094bc_L110
    b ov001_022094bc_L118
ov001_022094bc_Lf8:
    mov r0, #3
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L100:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L108:
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L110:
    mov r0, #2
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L118:
    mov r0, #6
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L120:
    mov r0, #4
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L128:
    mov r0, #5
    ldmia sp!, {r4, r5, r6, pc}
ov001_022094bc_L130:
    mvn r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
