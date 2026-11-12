/* ov001 row 0x021ff618: 348 bytes.
 *
 * What it does: 85 instructions; 16 call(s) to 0x0202a634, 0x02202360, 0x0220178c, +13 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 16 calls (85 instructions, 16 calls, 14 branches, 5 back edges, 2 literal slots).
 *
 *   pool +0x154 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x158 -> constant 0x00000201 (image word 0x00000201)
 *   branch +0x30 -> +0x48
 *   branch +0x44 -> +0x74
 *   branch +0x50 -> +0x6c
 *   branch +0x68 -> +0x74
 *   branch +0x78 -> +0xb8
 *   branch +0xb0 -> +0xb8
 *   branch +0xc4 -> +0x130
 *   branch +0xdc -> +0x124
 *   branch +0xe8 -> +0x100
 *   branch +0xfc -> +0x124
 *   branch +0x10c -> +0x120
 *   branch +0x11c -> +0x124
 *   branch +0x128 -> +0x130
 *   branch +0x138 -> +0x14c
 *   test +0x2c cmp r1, #0
 *   test +0x4c tst r1, #2
 *   test +0x74 cmp r7, #0
 *   test +0xac cmp r0, #0
 *   test +0xc0 cmp r0, #0
 *   test +0xcc cmp r0, #4
 *   test +0xd8 cmpne r0, #10
 *   test +0xe4 cmp r0, #0
 *   test +0x108 tst r1, r0
 *   test +0x124 cmp r5, #0
 *   test +0x134 cmp r0, #2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff618; the literal pool and
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

extern void native_fn_0202a634(void);
extern void ov001_table_f0_entry_02202360(void);
extern void native_fn_0220178c(void);
extern void native_fn_021f949c(void);
extern void native_fn_02202420(void);
extern void native_fn_0220451c(void);
extern void native_fn_021fe3dc(void);
extern void native_fn_022023c4(void);
extern void native_fn_021fd858(void);
extern void native_fn_021e13b8(void);
extern void native_fn_02203418(void);
extern void native_fn_0220054c(void);
extern void native_fn_02201438(void);
extern void native_fn_022139f8(void);


asm u32 native_ov001_021ff618 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    bl native_fn_0202a634
    ldr r1, =0x02239c10
    mov r4, r0
    ldrsb r0, [r1, #12]
    mov r5, #0
    bl ov001_table_f0_entry_02202360
    ldr r1, =0x02239c10
    mov r6, r0
    ldr r1, [r1, #0x10]
    mov r7, r5
    cmp r1, #0
    beq ov001_021ff618_L48
    bl native_fn_0220178c
    ldr r0, =0x02239c10
    mov r1, r5
    str r1, [r0, #0x10]
    b ov001_021ff618_L74
ov001_021ff618_L48:
    ldrh r1, [r4, #2]
    tst r1, #2
    beq ov001_021ff618_L6c
    mov r0, #85
    mov r1, #1
    str r7, [r6]
    bl native_fn_021f949c
    mov r7, #1
    b ov001_021ff618_L74
ov001_021ff618_L6c:
    bl native_fn_02202420
    mov r7, r0
ov001_021ff618_L74:
    cmp r7, #0
    beq ov001_021ff618_Lb8
    ldr r2, [r6]
    ldr r1, [r6, #0x4]
    add r0, r6, #24
    sub r1, r2, r1
    bl native_fn_0220451c
    ldr r1, =0x02239c10
    mov r0, #1
    ldrsb r1, [r1, #12]
    bl native_fn_021fe3dc
    mov r0, #8
    bl native_fn_022023c4
    ldrb r0, [r6, #0x11]
    cmp r0, #0
    beq ov001_021ff618_Lb8
    bl native_fn_021fd858
ov001_021ff618_Lb8:
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #0
    bne ov001_021ff618_L130
    bl native_fn_021e13b8
    cmp r0, #4
    ldrne r0, =0x02239c10
    ldrneb r0, [r0, #0xa]
    cmpne r0, #10
    beq ov001_021ff618_L124
    bl native_fn_02203418
    cmp r0, #0
    beq ov001_021ff618_L100
    mov r0, #0
    str r0, [r6]
    bl native_fn_0220054c
    mov r5, r0
    b ov001_021ff618_L124
ov001_021ff618_L100:
    ldrh r1, [r4, #2]
    ldr r0, =0x00000201
    tst r1, r0
    beq ov001_021ff618_L120
    ldr r0, [r6]
    bl native_fn_0220054c
    mov r5, r0
    b ov001_021ff618_L124
ov001_021ff618_L120:
    bl native_fn_02201438
ov001_021ff618_L124:
    cmp r5, #0
    beq ov001_021ff618_L130
    bl native_fn_0220178c
ov001_021ff618_L130:
    bl native_fn_022139f8
    cmp r0, #2
    bne ov001_021ff618_L14c
    ldr r0, =0x02239c10
    mov r1, #24
    strb r1, [r0, #0xa]
    mov r5, #2
ov001_021ff618_L14c:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
