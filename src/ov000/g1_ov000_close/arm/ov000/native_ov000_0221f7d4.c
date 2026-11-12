/* ov000 row 0x0221f7d4: 204 bytes.
 *
 * What it does: 50 instructions; 8 call(s) to 0x0207cd98, 0x02062a10, 0x02062a10, +5 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc8 -> constant 0x022463b0 (image word 0x022463b0)
 *   branch +0x10 -> +0xc0
 *   branch +0x28 -> +0xb4
 *   branch +0x38 -> +0x50
 *   branch +0x4c -> +0xb4
 *   branch +0x74 -> +0xb4
 *   branch +0x80 -> +0x98
 *   branch +0x94 -> +0xb4
 *   back edge +0xbc -> +0x1c
 *   test +0x0c cmp r4, #100
 *   test +0x34 cmp r7, r0
 *   test +0x48 cmp r0, #2
 *   test +0x70 cmp r1, r0
 *   test +0x7c cmp r0, #2
 *   test +0x90 cmp r0, #2
 *   test +0xa8 cmp r0, #0
 *   test +0xb8 cmp r4, #100
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221f7d4; the literal pool and
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

extern void native_fn_0207cd98(void);
extern void native_fn_02062a10(void);
extern void native_fn_02220778(void);


asm u32 native_ov000_0221f7d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    add r4, r0, #1
    mov r7, r1
    cmp r4, #100
    bge ov000_0221f7d4_Lc0
    ldr r9, =0x022463b0
    mov r8, #132
ov000_0221f7d4_L1c:
    mov r0, r4
    bl native_fn_0207cd98
    movs r5, r0
    beq ov000_0221f7d4_Lb4
    bl native_fn_02062a10
    ldrb r0, [r0, #0x1b]
    cmp r7, r0
    beq ov000_0221f7d4_L50
    mov r0, r5
    bl native_fn_02062a10
    ldrb r0, [r0, #0x1b]
    cmp r0, #2
    bne ov000_0221f7d4_Lb4
ov000_0221f7d4_L50:
    ldr r0, [r9, #0xc]
    ldr r1, [r9, #0x1c]
    rsb r0, r0, #1
    mla r6, r0, r8, r1
    mov r0, r5
    bl native_fn_02062a10
    ldr r1, [r6, #0x14]
    ldr r0, [r0, #0x14]
    cmp r1, r0
    beq ov000_0221f7d4_Lb4
    ldrb r0, [r6, #0x1b]
    cmp r0, #2
    bne ov000_0221f7d4_L98
    mov r0, r5
    bl native_fn_02062a10
    ldrb r0, [r0, #0x1b]
    cmp r0, #2
    beq ov000_0221f7d4_Lb4
ov000_0221f7d4_L98:
    mov r0, r5
    bl native_fn_02062a10
    ldrsh r0, [r0, #24]
    bl native_fn_02220778
    cmp r0, #0
    movne r0, r4
    ldmneia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov000_0221f7d4_Lb4:
    add r4, r4, #1
    cmp r4, #100
    blt ov000_0221f7d4_L1c
ov000_0221f7d4_Lc0:
    mvn r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
