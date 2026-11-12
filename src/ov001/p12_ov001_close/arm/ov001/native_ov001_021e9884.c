/* ov001 row 0x021e9884: 476 bytes.
 *
 * What it does: 118 instructions; 27 call(s) to 0x021d75d4, 0x021d75d4, 0x021d94cc, +24 more; loops (back edge at +0x24); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 27 calls (118 instructions, 27 calls, 18 branches, 27 back edges, 1 literal slot).
 *
 *   pool +0x1d8 -> constant 0x02238d7c (image word 0x02238d7c)
 *   branch +0x08 -> +0x44
 *   branch +0x1c -> +0x2c
 *   branch +0x28 -> +0x34
 *   branch +0x48 -> +0x130
 *   branch +0x5c -> +0x8c
 *   branch +0x70 -> +0x80
 *   branch +0x7c -> +0xc8
 *   branch +0x88 -> +0xc8
 *   branch +0x9c -> +0xac
 *   branch +0xa8 -> +0xc8
 *   branch +0xb0 -> +0xc0
 *   branch +0xbc -> +0xc8
 *   branch +0x10c -> +0x120
 *   branch +0x134 -> +0x150
 *   branch +0x168 -> +0x178
 *   branch +0x174 -> +0x194
 *   branch +0x17c -> +0x18c
 *   branch +0x188 -> +0x194
 *   test +0x04 cmp r0, #1
 *   test +0x18 cmp r0, #0
 *   test +0x44 cmp r0, #2
 *   test +0x58 cmp r0, #0
 *   test +0x6c cmp r0, #1
 *   test +0x98 cmp r0, #2
 *   test +0xac cmp r0, #1
 *   test +0x108 cmp r0, #0
 *   test +0x130 cmp r0, #4
 *   test +0x150 cmp r0, #3
 *   test +0x164 cmp r0, #2
 *   test +0x178 cmp r0, #1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e9884; the literal pool and
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

extern void native_fn_021d75d4(void);
extern void native_fn_021d94cc(void);
extern void native_fn_021dbaac(void);
extern void native_fn_021db9e0(void);
extern void native_fn_02042c2c(void);
extern void native_fn_021d77b0(void);
extern void native_fn_02041f74(void);
extern void native_fn_021d7814(void);


asm u32 native_ov001_021e9884 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    cmp r0, #1
    bne ov001_021e9884_L44
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    bne ov001_021e9884_L2c
    mov r0, #3
    bl native_fn_021d75d4
    b ov001_021e9884_L34
ov001_021e9884_L2c:
    mov r0, #4
    bl native_fn_021d75d4
ov001_021e9884_L34:
    mov r0, #1
    mov r1, r0
    bl native_fn_021d94cc
    ldmia sp!, {r3, pc}
ov001_021e9884_L44:
    cmp r0, #2
    bne ov001_021e9884_L130
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_021dbaac
    cmp r0, #0
    beq ov001_021e9884_L8c
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #1
    bne ov001_021e9884_L80
    mov r0, #8
    bl native_fn_021d75d4
    b ov001_021e9884_Lc8
ov001_021e9884_L80:
    mov r0, #9
    bl native_fn_021d75d4
    b ov001_021e9884_Lc8
ov001_021e9884_L8c:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_021db9e0
    cmp r0, #2
    bne ov001_021e9884_Lac
    mov r0, #7
    bl native_fn_021d75d4
    b ov001_021e9884_Lc8
ov001_021e9884_Lac:
    cmp r0, #1
    bne ov001_021e9884_Lc0
    mov r0, #6
    bl native_fn_021d75d4
    b ov001_021e9884_Lc8
ov001_021e9884_Lc0:
    mov r0, #5
    bl native_fn_021d75d4
ov001_021e9884_Lc8:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_02042c2c
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d77b0
    ldr r0, =0x02238d7c
    mov r1, #0
    ldr r0, [r0, #0x60]
    bl native_fn_02041f74
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d7814
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    bne ov001_021e9884_L120
    mov r0, #1
    mov r1, #0
    bl native_fn_021d94cc
    ldmia sp!, {r3, pc}
ov001_021e9884_L120:
    mov r0, #0
    mov r1, #1
    bl native_fn_021d94cc
    ldmia sp!, {r3, pc}
ov001_021e9884_L130:
    cmp r0, #4
    bne ov001_021e9884_L150
    mov r0, #13
    bl native_fn_021d75d4
    mov r0, #1
    mov r1, r0
    bl native_fn_021d94cc
    ldmia sp!, {r3, pc}
ov001_021e9884_L150:
    cmp r0, #3
    ldmneia sp!, {r3, pc}
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl native_fn_021db9e0
    cmp r0, #2
    bne ov001_021e9884_L178
    mov r0, #12
    bl native_fn_021d75d4
    b ov001_021e9884_L194
ov001_021e9884_L178:
    cmp r0, #1
    bne ov001_021e9884_L18c
    mov r0, #11
    bl native_fn_021d75d4
    b ov001_021e9884_L194
ov001_021e9884_L18c:
    mov r0, #10
    bl native_fn_021d75d4
ov001_021e9884_L194:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl native_fn_02042c2c
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d77b0
    ldr r0, =0x02238d7c
    mov r1, #0
    ldr r0, [r0, #0x54]
    bl native_fn_02041f74
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d7814
    mov r0, #1
    mov r1, r0
    bl native_fn_021d94cc
    ldmia sp!, {r3, pc}
}
