/* ov001 row 0x0220046c: 224 bytes.
 *
 * What it does: 53 instructions; 9 call(s) to 0x0202a634, 0x02202360, 0x02203418, +6 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (53 instructions, 9 calls, 11 branches, 5 back edges, 3 literal slots).
 *
 *   pool +0xd4 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0xd8 -> constant 0x00000ff7 (image word 0x00000ff7)
 *   pool +0xdc -> native_data_0222ed34 (image word 0x0222ed34)
 *   branch +0x28 -> +0x3c
 *   branch +0x38 -> +0xcc
 *   branch +0x5c -> +0xbc
 *   branch +0x60 -> +0x78
 *   branch +0x64 -> +0xa8
 *   branch +0x68 -> +0xa8
 *   branch +0x6c -> +0xb4
 *   branch +0x70 -> +0xa8
 *   branch +0x74 -> +0xa8
 *   branch +0xa4 -> +0xbc
 *   branch +0xb0 -> +0xbc
 *   test +0x24 cmp r0, #0
 *   test +0x34 tst r1, r0
 *   test +0x54 cmp r1, #5
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220046c; the literal pool and
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
extern void native_fn_02202360(void);
extern void native_fn_02203418(void);
extern void native_fn_02045680(void);
extern void native_fn_021fd84c(void);
extern void native_fn_021fea54(void);
extern void native_fn_02204590(void);
extern u8 native_data_0222ed34[];
extern void native_fn_0204b61c(void);


asm u32 native_ov001_0220046c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    bl native_fn_0202a634
    ldr r1, =0x02239c10
    mov r5, r0
    ldrsb r0, [r1, #12]
    bl native_fn_02202360
    mov r4, r0
    mov r6, #0
    bl native_fn_02203418
    cmp r0, #0
    bne ov001_0220046c_L3c
    ldrh r1, [r5, #2]
    ldr r0, =0x00000ff7
    tst r1, r0
    beq ov001_0220046c_Lcc
ov001_0220046c_L3c:
    mov r0, #0
    bl native_fn_02045680
    bl native_fn_021fd84c
    bl native_fn_021fea54
    ldr r0, =0x02239c10
    ldrsb r1, [r0, #12]
    cmp r1, #5
    addls pc, pc, r1, lsl #2
    b ov001_0220046c_Lbc
    b ov001_0220046c_L78
    b ov001_0220046c_La8
    b ov001_0220046c_La8
    b ov001_0220046c_Lb4
    b ov001_0220046c_La8
    b ov001_0220046c_La8
ov001_0220046c_L78:
    mov r0, #0
    bl native_fn_02202360
    add r0, r0, #24
    mov r1, #123
    bl native_fn_02204590
    ldr r1, =0x02239c10
    mov r3, #3
    ldr r0, =native_data_0222ed34
    mov r2, #1
    strb r3, [r1, #0xa]
    strb r2, [r0, #0x2]
    b ov001_0220046c_Lbc
ov001_0220046c_La8:
    mov r1, #5
    strb r1, [r0, #0xa]
    b ov001_0220046c_Lbc
ov001_0220046c_Lb4:
    mov r1, #7
    strb r1, [r0, #0xa]
ov001_0220046c_Lbc:
    add r0, r4, #24
    mov r1, #1
    bl native_fn_0204b61c
    mov r6, #1
ov001_0220046c_Lcc:
    mov r0, r6
    ldmia sp!, {r4, r5, r6, pc}
}
