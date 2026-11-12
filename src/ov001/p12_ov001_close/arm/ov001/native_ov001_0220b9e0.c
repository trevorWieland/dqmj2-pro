/* ov001 row 0x0220b9e0: 412 bytes.
 *
 * What it does: 103 instructions; 28 call(s) to 0x0220b74c, 0x0220b794, 0x021dbac8, +25 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 28 calls (103 instructions, 28 calls, 20 branches, 28 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0xd4
 *   branch +0x28 -> +0x4c
 *   branch +0x30 -> +0x40
 *   branch +0x3c -> +0x98
 *   branch +0x48 -> +0x98
 *   branch +0x6c -> +0x7c
 *   branch +0x78 -> +0x98
 *   branch +0x80 -> +0x90
 *   branch +0x8c -> +0x98
 *   branch +0xa0 -> +0xbc
 *   branch +0xf0 -> +0x118
 *   branch +0xfc -> +0x10c
 *   branch +0x108 -> +0x148
 *   branch +0x114 -> +0x148
 *   branch +0x11c -> +0x12c
 *   branch +0x128 -> +0x148
 *   branch +0x130 -> +0x140
 *   branch +0x13c -> +0x148
 *   branch +0x14c -> +0x160
 *   branch +0x15c -> +0x16c
 *   test +0x14 cmp r1, #4
 *   test +0x24 cmp r0, #0
 *   test +0x2c cmp r5, #0
 *   test +0x68 cmp r4, #0
 *   test +0x7c cmp r0, #0
 *   test +0x98 cmp r5, #0
 *   test +0xec cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x118 cmp r4, #2
 *   test +0x12c cmp r4, #1
 *   test +0x148 cmp r5, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220b9e0; the literal pool and
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

extern void native_fn_0220b74c(void);
extern void native_fn_0220b794(void);
extern void native_fn_021dbac8(void);
extern void native_fn_021d75d4(void);
extern void native_fn_021dba58(void);
extern void native_fn_021d77b0(void);
extern void native_fn_021d94cc(void);
extern void native_fn_021db438(void);
extern void native_fn_021db9e0(void);
extern void native_fn_021dbaac(void);
extern void native_fn_02042c2c(void);
extern void native_fn_02041f74(void);
extern void native_fn_021d7814(void);


asm u32 native_ov001_0220b9e0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_0220b74c
    mov r5, r0
    bl native_fn_0220b794
    mov r1, r0
    cmp r1, #4
    mov r0, r5
    bne ov001_0220b9e0_Ld4
    bl native_fn_021dbac8
    cmp r0, #0
    beq ov001_0220b9e0_L4c
    cmp r5, #0
    bne ov001_0220b9e0_L40
    mov r0, #25
    bl native_fn_021d75d4
    b ov001_0220b9e0_L98
ov001_0220b9e0_L40:
    mov r0, #24
    bl native_fn_021d75d4
    b ov001_0220b9e0_L98
ov001_0220b9e0_L4c:
    mov r0, r5
    mov r1, #2
    bl native_fn_021dba58
    mov r4, r0
    mov r0, r5
    mov r1, #1
    bl native_fn_021dba58
    cmp r4, #0
    beq ov001_0220b9e0_L7c
    mov r0, #23
    bl native_fn_021d75d4
    b ov001_0220b9e0_L98
ov001_0220b9e0_L7c:
    cmp r0, #0
    beq ov001_0220b9e0_L90
    mov r0, #22
    bl native_fn_021d75d4
    b ov001_0220b9e0_L98
ov001_0220b9e0_L90:
    mov r0, #21
    bl native_fn_021d75d4
ov001_0220b9e0_L98:
    cmp r5, #0
    mvn r0, #0
    bne ov001_0220b9e0_Lbc
    mov r1, #737280
    bl native_fn_021d77b0
    mov r0, #1
    mov r1, #0
    bl native_fn_021d94cc
    ldmia sp!, {r4, r5, r6, pc}
ov001_0220b9e0_Lbc:
    mov r1, #0
    bl native_fn_021d77b0
    mov r0, #0
    mov r1, #1
    bl native_fn_021d94cc
    ldmia sp!, {r4, r5, r6, pc}
ov001_0220b9e0_Ld4:
    bl native_fn_021db438
    mov r6, r0
    bl native_fn_021db9e0
    mov r4, r0
    mov r0, r6
    bl native_fn_021dbaac
    cmp r0, #0
    beq ov001_0220b9e0_L118
    ldrb r0, [r6, #0x31e]
    cmp r0, #0
    bne ov001_0220b9e0_L10c
    mov r0, #18
    bl native_fn_021d75d4
    b ov001_0220b9e0_L148
ov001_0220b9e0_L10c:
    mov r0, #17
    bl native_fn_021d75d4
    b ov001_0220b9e0_L148
ov001_0220b9e0_L118:
    cmp r4, #2
    bne ov001_0220b9e0_L12c
    mov r0, #16
    bl native_fn_021d75d4
    b ov001_0220b9e0_L148
ov001_0220b9e0_L12c:
    cmp r4, #1
    bne ov001_0220b9e0_L140
    mov r0, #15
    bl native_fn_021d75d4
    b ov001_0220b9e0_L148
ov001_0220b9e0_L140:
    mov r0, #14
    bl native_fn_021d75d4
ov001_0220b9e0_L148:
    cmp r5, #0
    bne ov001_0220b9e0_L160
    mov r0, #1
    mov r1, #0
    bl native_fn_021d94cc
    b ov001_0220b9e0_L16c
ov001_0220b9e0_L160:
    mov r0, #0
    mov r1, #1
    bl native_fn_021d94cc
ov001_0220b9e0_L16c:
    mov r0, r6
    bl native_fn_02042c2c
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d77b0
    mov r0, r6
    mov r1, #0
    bl native_fn_02041f74
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d7814
    ldmia sp!, {r4, r5, r6, pc}
}
