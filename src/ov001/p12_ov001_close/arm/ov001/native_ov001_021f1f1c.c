/* ov001 row 0x021f1f1c: 516 bytes.
 *
 * What it does: 128 instructions; 25 call(s) to 0x021dbaac, 0x021d75d4, 0x021d75d4, +22 more; loops (back edge at +0x40); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 25 calls (128 instructions, 25 calls, 21 branches, 25 back edges, 1 literal slot).
 *
 *   pool +0x200 -> constant 0x0223989c (image word 0x0223989c)
 *   branch +0x10 -> +0x24
 *   branch +0x20 -> +0x11c
 *   branch +0x34 -> +0x11c
 *   branch +0x48 -> +0x78
 *   branch +0x5c -> +0x6c
 *   branch +0x68 -> +0xb4
 *   branch +0x74 -> +0xb4
 *   branch +0x88 -> +0x98
 *   branch +0x94 -> +0xb4
 *   branch +0x9c -> +0xac
 *   branch +0xa8 -> +0xb4
 *   branch +0xf8 -> +0x10c
 *   branch +0x12c -> +0x15c
 *   branch +0x140 -> +0x150
 *   branch +0x14c -> +0x1b8
 *   branch +0x158 -> +0x1b8
 *   branch +0x18c -> +0x19c
 *   branch +0x198 -> +0x1b8
 *   branch +0x1a0 -> +0x1b0
 *   branch +0x1ac -> +0x1b8
 *   branch +0x1cc -> +0x1e8
 *   test +0x1c cmp r1, #0
 *   test +0x30 cmp r0, #7
 *   test +0x44 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x84 cmp r0, #2
 *   test +0x98 cmp r0, #1
 *   test +0xf4 cmp r0, #0
 *   test +0x128 cmp r0, #0
 *   test +0x13c cmp r0, #1
 *   test +0x188 cmp r4, #0
 *   test +0x19c cmp r0, #0
 *   test +0x1c4 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f1f1c; the literal pool and
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

extern void native_fn_021dbaac(void);
extern void native_fn_021d75d4(void);
extern void native_fn_021db9e0(void);
extern void native_fn_02042c2c(void);
extern void native_fn_021d77b0(void);
extern void native_fn_02041f74(void);
extern void native_fn_021d7814(void);
extern void native_fn_021d94cc(void);
extern void native_fn_021dba58(void);


asm u32 native_ov001_021f1f1c (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldrh r1, [r0, #8]
    mov r1, r1, lsl #16
    movs r1, r1, lsr #28
    beq ov001_021f1f1c_L24
    ldr r1, =0x0223989c
    ldrb r1, [r1, #0x8]
    cmp r1, #0
    beq ov001_021f1f1c_L11c
ov001_021f1f1c_L24:
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #7
    beq ov001_021f1f1c_L11c
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    bl native_fn_021dbaac
    cmp r0, #0
    beq ov001_021f1f1c_L78
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    bne ov001_021f1f1c_L6c
    mov r0, #18
    bl native_fn_021d75d4
    b ov001_021f1f1c_Lb4
ov001_021f1f1c_L6c:
    mov r0, #17
    bl native_fn_021d75d4
    b ov001_021f1f1c_Lb4
ov001_021f1f1c_L78:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    bl native_fn_021db9e0
    cmp r0, #2
    bne ov001_021f1f1c_L98
    mov r0, #16
    bl native_fn_021d75d4
    b ov001_021f1f1c_Lb4
ov001_021f1f1c_L98:
    cmp r0, #1
    bne ov001_021f1f1c_Lac
    mov r0, #15
    bl native_fn_021d75d4
    b ov001_021f1f1c_Lb4
ov001_021f1f1c_Lac:
    mov r0, #14
    bl native_fn_021d75d4
ov001_021f1f1c_Lb4:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    bl native_fn_02042c2c
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d77b0
    ldr r0, =0x0223989c
    mov r1, #0
    ldr r0, [r0, #0x80]
    bl native_fn_02041f74
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d7814
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    bne ov001_021f1f1c_L10c
    mov r0, #1
    mov r1, #0
    bl native_fn_021d94cc
    ldmia sp!, {r4, pc}
ov001_021f1f1c_L10c:
    mov r0, #0
    mov r1, #1
    bl native_fn_021d94cc
    ldmia sp!, {r4, pc}
ov001_021f1f1c_L11c:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    bl native_fn_021dbaac
    cmp r0, #0
    beq ov001_021f1f1c_L15c
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    ldrb r0, [r0, #0x31e]
    cmp r0, #1
    bne ov001_021f1f1c_L150
    mov r0, #24
    bl native_fn_021d75d4
    b ov001_021f1f1c_L1b8
ov001_021f1f1c_L150:
    mov r0, #25
    bl native_fn_021d75d4
    b ov001_021f1f1c_L1b8
ov001_021f1f1c_L15c:
    ldr r0, =0x0223989c
    mov r1, #2
    ldr r0, [r0, #0x80]
    ldrb r0, [r0, #0x31e]
    bl native_fn_021dba58
    ldr r1, =0x0223989c
    mov r4, r0
    ldr r0, [r1, #0x80]
    mov r1, #1
    ldrb r0, [r0, #0x31e]
    bl native_fn_021dba58
    cmp r4, #0
    beq ov001_021f1f1c_L19c
    mov r0, #23
    bl native_fn_021d75d4
    b ov001_021f1f1c_L1b8
ov001_021f1f1c_L19c:
    cmp r0, #0
    beq ov001_021f1f1c_L1b0
    mov r0, #22
    bl native_fn_021d75d4
    b ov001_021f1f1c_L1b8
ov001_021f1f1c_L1b0:
    mov r0, #21
    bl native_fn_021d75d4
ov001_021f1f1c_L1b8:
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x80]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    mvn r0, #0
    bne ov001_021f1f1c_L1e8
    mov r1, #737280
    bl native_fn_021d77b0
    mov r0, #1
    mov r1, #0
    bl native_fn_021d94cc
    ldmia sp!, {r4, pc}
ov001_021f1f1c_L1e8:
    mov r1, #0
    bl native_fn_021d77b0
    mov r0, #0
    mov r1, #1
    bl native_fn_021d94cc
    ldmia sp!, {r4, pc}
}
