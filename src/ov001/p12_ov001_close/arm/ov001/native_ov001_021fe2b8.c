/* ov001 row 0x021fe2b8: 280 bytes.
 *
 * What it does: 68 instructions; 9 call(s) to 0x02049ad0, 0x020852c8, 0x02203000, +6 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (68 instructions, 9 calls, 9 branches, 6 back edges, 2 literal slots).
 *
 *   pool +0x110 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x114 -> native_data_0222ed34 (image word 0x0222ed34)
 *   branch +0x1c -> +0x100
 *   branch +0x68 -> +0x80
 *   branch +0x70 -> +0x88
 *   branch +0x78 -> +0x90
 *   branch +0x7c -> +0xb8
 *   branch +0x84 -> +0xb8
 *   branch +0x8c -> +0xb8
 *   branch +0x98 -> +0xb4
 *   branch +0xbc -> +0xc8
 *   test +0x18 cmp r1, #0
 *   test +0x2c cmp r0, #0
 *   test +0x4c cmp r0, #11
 *   test +0x64 cmp r7, #0
 *   test +0x6c cmp r7, #1
 *   test +0x74 cmp r7, #2
 *   test +0x94 cmp r0, #0
 *   test +0xb8 cmp r6, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fe2b8; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_020852c8(void);
extern u8 native_data_0222ed34[];
extern void native_fn_02203000(void);
extern void native_fn_021feba4(void);
extern void native_fn_0204a04c(void);
extern void native_fn_02085270(void);
extern void native_fn_02085418(void);
extern void native_fn_021fec1c(void);


asm u32 native_ov001_021fe2b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r7, r0
    mov r0, #22
    mov r6, r1
    bl native_fn_02049ad0
    ldr r1, [r0]
    cmp r1, #0
    beq ov001_021fe2b8_L100
    ldr r0, =0x02239c10
    ldr r4, [r1, #0x4]
    ldrb r0, [r0]
    cmp r0, #0
    moveq r1, #1
    movne r1, #3
    mov r0, r4
    and r1, r1, #255
    bl native_fn_020852c8
    ldr r0, =0x02239c10
    ldrb r0, [r0, #0xa]
    cmp r0, #11
    ldrne r0, =native_data_0222ed34
    movne r1, #1
    ldreq r0, =native_data_0222ed34
    moveq r1, #0
    str r1, [r0, #0x4]
    cmp r7, #0
    beq ov001_021fe2b8_L80
    cmp r7, #1
    beq ov001_021fe2b8_L88
    cmp r7, #2
    beq ov001_021fe2b8_L90
    b ov001_021fe2b8_Lb8
ov001_021fe2b8_L80:
    mov r5, #4
    b ov001_021fe2b8_Lb8
ov001_021fe2b8_L88:
    mov r5, #5
    b ov001_021fe2b8_Lb8
ov001_021fe2b8_L90:
    bl native_fn_02203000
    cmp r0, #0
    bne ov001_021fe2b8_Lb4
    mov r0, r4
    mov r1, #3
    bl native_fn_020852c8
    ldr r0, =native_data_0222ed34
    mov r1, #0
    str r1, [r0, #0x4]
ov001_021fe2b8_Lb4:
    mov r5, #31
ov001_021fe2b8_Lb8:
    cmp r6, #0
    beq ov001_021fe2b8_Lc8
    mov r0, r7
    bl native_fn_021feba4
ov001_021fe2b8_Lc8:
    ldr r6, =0x02239c10
    mov r0, r4
    mov r3, r5
    mov r1, #5
    mov r2, #2
    strb r7, [r6, #0xe]
    bl native_fn_0204a04c
    add r0, r4, #60
    mov r1, #8
    mov r2, #0
    bl native_fn_02085270
    mov r0, r4
    mov r1, #3
    bl native_fn_02085418
ov001_021fe2b8_L100:
    ldr r0, =native_data_0222ed34
    ldr r0, [r0, #0x4]
    bl native_fn_021fec1c
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
