/* ov001 row 0x021f71ec: 432 bytes.
 *
 * What it does: 105 instructions; 10 call(s) to 0x021db438, 0x021f6e90, 0x021f2120, +7 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (105 instructions, 10 calls, 13 branches, 8 back edges, 3 literal slots).
 *
 *   pool +0x1a4 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x1a8 -> constant 0x02239964 (image word 0x02239964)
 *   pool +0x1ac -> constant 0x02239960 (image word 0x02239960)
 *   branch +0x38 -> +0x90
 *   branch +0x70 -> +0x80
 *   branch +0x8c -> +0x19c
 *   branch +0x94 -> +0x128
 *   branch +0xb4 -> +0xcc
 *   back edge +0xdc -> +0xac
 *   branch +0xe4 -> +0x19c
 *   branch +0x100 -> +0x19c
 *   branch +0x124 -> +0x19c
 *   branch +0x12c -> +0x168
 *   branch +0x140 -> +0x19c
 *   branch +0x154 -> +0x19c
 *   branch +0x164 -> +0x19c
 *   branch +0x16c -> +0x19c
 *   branch +0x188 -> +0x19c
 *   test +0x14 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x90 cmp r0, #10
 *   test +0xb0 cmp r0, #0
 *   test +0xc4 cmp r0, #0
 *   test +0xd0 cmp r4, #3
 *   test +0xe0 cmp r5, #0
 *   test +0xfc cmp r1, #45
 *   test +0x128 cmp r0, #20
 *   test +0x13c cmp r0, #0
 *   test +0x150 cmp r0, #0
 *   test +0x168 cmp r0, #100
 *   test +0x17c cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f71ec; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021f6e90(void);
extern void native_fn_021f2120(void);
extern void native_fn_021f5cc0(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);
extern void native_fn_022168e8(void);
extern void native_fn_021f4210(void);


asm u32 native_ov001_021f71ec (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    ldr r0, =0x0223989c
    mov r1, #0
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r8, #0
    movne r8, #1
    mov r0, r8
    bl ov001_side_slot_record_021db438
    ldr r1, =0x0223989c
    mov r7, r0
    ldrb r0, [r1, #0x38]
    cmp r0, #0
    bne ov001_021f71ec_L90
    ldrb r0, [r1, #0x10]
    ldr r2, =0x02239964
    ldr r3, =0x02239960
    cmp r0, #0
    ldrne r4, [r1, #0x80]
    ldr r0, =0x0223989c
    moveq r4, #0
    ldr r0, [r0, #0x84]
    mov r1, r4
    bl native_fn_021f6e90
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    beq ov001_021f71ec_L80
    mov r0, r4
    mov r1, #176
    bl native_fn_021f2120
ov001_021f71ec_L80:
    ldr r0, =0x0223989c
    mov r1, #10
    strb r1, [r0, #0x38]
    b ov001_021f71ec_L19c
ov001_021f71ec_L90:
    cmp r0, #10
    bne ov001_021f71ec_L128
    mov r5, #0
    ldr r6, =0x02239960
    mov r4, r5
    mov r9, #1
    mov r10, #55
ov001_021f71ec_Lac:
    ldrb r0, [r6]
    cmp r0, #0
    beq ov001_021f71ec_Lcc
    mov r0, r7
    mov r1, r10
    bl native_fn_021f5cc0
    cmp r0, #0
    moveq r5, r9
ov001_021f71ec_Lcc:
    add r4, r4, #1
    cmp r4, #3
    add r6, r6, #1
    add r7, r7, #1088
    blt ov001_021f71ec_Lac
    cmp r5, #0
    bne ov001_021f71ec_L19c
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x37]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x37]
    cmp r1, #45
    blo ov001_021f71ec_L19c
    mov r1, r8
    mov r0, #0
    bl native_fn_021dbb14
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x38]
    mov r1, #0
    strb r1, [r0, #0x37]
    b ov001_021f71ec_L19c
ov001_021f71ec_L128:
    cmp r0, #20
    bne ov001_021f71ec_L168
    mov r1, r8
    mov r0, #0
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_021f71ec_L19c
    mov r1, r8
    mov r0, #0
    bl native_fn_022168e8
    cmp r0, #0
    beq ov001_021f71ec_L19c
    ldr r0, =0x0223989c
    mov r1, #100
    strb r1, [r0, #0x38]
    b ov001_021f71ec_L19c
ov001_021f71ec_L168:
    cmp r0, #100
    bne ov001_021f71ec_L19c
    mov r0, #0
    strb r0, [r1, #0x38]
    ldrb r0, [r1, #0x10]
    cmp r0, #0
    moveq r0, #14
    streqb r0, [r1, #0x1b]
    beq ov001_021f71ec_L19c
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
    strb r1, [r0, #0x1b]
ov001_021f71ec_L19c:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
