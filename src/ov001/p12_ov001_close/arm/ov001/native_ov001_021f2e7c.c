/* ov001 row 0x021f2e7c: 512 bytes.
 *
 * What it does: 124 instructions; 15 call(s) to 0x0202ac08, 0x021eea10, 0x0205d790, +12 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 15 calls (124 instructions, 15 calls, 16 branches, 15 back edges, 4 literal slots).
 *
 *   pool +0x1f0 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x1f4 -> constant 0x0223992c (image word 0x0223992c)
 *   pool +0x1f8 -> native_data_0222ed16 (image word 0x0222ed16)
 *   pool +0x1fc -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x14 -> +0x140
 *   branch +0x64 -> +0x120
 *   branch +0x74 -> +0xec
 *   branch +0x8c -> +0xa4
 *   branch +0xa0 -> +0xec
 *   branch +0xf8 -> +0x120
 *   back edge +0x12c -> +0x58
 *   branch +0x13c -> +0x1e4
 *   branch +0x144 -> +0x194
 *   branch +0x154 -> +0x164
 *   branch +0x160 -> +0x1e4
 *   branch +0x174 -> +0x184
 *   branch +0x180 -> +0x1e4
 *   branch +0x190 -> +0x1e4
 *   branch +0x198 -> +0x1e4
 *   branch +0x1a8 -> +0x1b0
 *   branch +0x1c0 -> +0x1c8
 *   test +0x10 cmp r0, #0
 *   test +0x60 cmp r1, r0
 *   test +0x70 cmp r0, r5
 *   test +0xf4 cmp r0, r5
 *   test +0x124 cmp r9, #3
 *   test +0x140 cmp r0, #10
 *   test +0x150 cmp r0, r1
 *   test +0x15c cmp r0, #0
 *   test +0x170 cmp r0, r1
 *   test +0x17c cmp r0, #0
 *   test +0x194 cmp r0, #100
 *   test +0x1a4 cmp r0, r1
 *   test +0x1bc cmp r0, r1
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f2e7c; the literal pool and
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

extern void native_fn_0202ac08(void);
extern u8 native_data_0222ed16[];
extern void native_fn_021eea10(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_02041f74(void);
extern void native_fn_021eedbc(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f2e7c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r1, =0x0223989c
    ldrb r0, [r1, #0x2]
    cmp r0, #0
    bne ov001_021f2e7c_L140
    mvn r3, #0
    strh r3, [r1, #106]
    ldrsh r2, [r1, #106]
    ldr r0, =0x0223992c
    strh r2, [r1, #104]
    str r3, [r1, #0x8c]
    str r3, [r1, #0x88]
    bl native_fn_0202ac08
    mov r9, #0
    ldr r10, =native_data_0222ed16
    ldr r6, =0x0223989c
    ldr r4, =0x66666667
    mov r8, r9
    add r7, sp, #4
    mov r11, r9
    mvn r5, #0
ov001_021f2e7c_L58:
    ldrh r1, [r6, #80]
    ldrsh r0, [r10]
    cmp r1, r0
    bne ov001_021f2e7c_L120
    ldrsh r0, [r10, #2]
    strh r0, [r6, #104]
    cmp r0, r5
    beq ov001_021f2e7c_Lec
    mov r1, r8
    bl native_fn_021eea10
    ldrsh r0, [r6, #104]
    bl native_fn_0205d790
    movs r2, r0
    bmi ov001_021f2e7c_La4
    ldrsh r0, [r6, #104]
    ldr r1, [r6, #0x84]
    bl ov001_effect_resource_create_021eec7c
    str r0, [r6, #0x88]
    b ov001_021f2e7c_Lec
ov001_021f2e7c_La4:
    ldr r0, [r6, #0x84]
    mov r1, r7
    bl native_fn_02041f74
    ldr r0, [r6, #0x84]
    ldrb r0, [r0, #0x31e]
    str r0, [sp]
    ldr r1, [sp, #0xc]
    ldrsh r0, [r6, #104]
    mov lr, r1, lsl #3
    ldr r1, [sp, #0x4]
    ldr r2, [sp, #0x8]
    smull r12, r3, r4, r14
    mov r12, lr, lsr #31
    add r3, r12, r3, asr #2
    bl native_fn_021eedbc
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r0, [r6, #0x88]
ov001_021f2e7c_Lec:
    ldrsh r0, [r10, #4]
    strh r0, [r6, #106]
    cmp r0, r5
    beq ov001_021f2e7c_L120
    mov r1, r11
    bl native_fn_021eea10
    ldrsh r0, [r6, #106]
    bl native_fn_0205d790
    mov r2, r0
    ldrsh r0, [r6, #106]
    ldr r1, [r6, #0x84]
    bl ov001_effect_resource_create_021eec7c
    str r0, [r6, #0x8c]
ov001_021f2e7c_L120:
    add r9, r9, #1
    cmp r9, #3
    add r10, r10, #6
    blt ov001_021f2e7c_L58
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x2]
    b ov001_021f2e7c_L1e4
ov001_021f2e7c_L140:
    cmp r0, #10
    bne ov001_021f2e7c_L194
    ldr r0, [r1, #0x88]
    mvn r1, #0
    cmp r0, r1
    beq ov001_021f2e7c_L164
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_021f2e7c_L1e4
ov001_021f2e7c_L164:
    ldr r0, =0x0223989c
    mvn r1, #0
    ldr r0, [r0, #0x8c]
    cmp r0, r1
    beq ov001_021f2e7c_L184
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_021f2e7c_L1e4
ov001_021f2e7c_L184:
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x2]
    b ov001_021f2e7c_L1e4
ov001_021f2e7c_L194:
    cmp r0, #100
    bne ov001_021f2e7c_L1e4
    ldrsh r0, [r1, #104]
    mvn r1, #0
    cmp r0, r1
    beq ov001_021f2e7c_L1b0
    bl native_fn_021eeb70
ov001_021f2e7c_L1b0:
    ldr r0, =0x0223989c
    mvn r1, #0
    ldrsh r0, [r0, #106]
    cmp r0, r1
    beq ov001_021f2e7c_L1c8
    bl native_fn_021eeb70
ov001_021f2e7c_L1c8:
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x2]
    mov r1, #3
    strb r1, [r0, #0x1b]
ov001_021f2e7c_L1e4:
    mov r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
