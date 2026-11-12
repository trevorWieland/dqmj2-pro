/* ov001 row 0x021ff96c: 660 bytes.
 *
 * What it does: 163 instructions; 26 call(s) to 0x0202a634, 0x02202360, 0x021db438, +23 more; loops (back edge at +0x08); returns through pop {r3, r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill (163 instructions, 26 calls, 27 branches, 12 back edges, 2 literal slots).
 *
 *   pool +0x28c -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x290 -> constant 0x00000201 (image word 0x00000201)
 *   branch +0x30 -> +0x190
 *   branch +0x48 -> +0xd4
 *   branch +0x4c -> +0xd4
 *   branch +0x50 -> +0x64
 *   branch +0x54 -> +0xcc
 *   branch +0x58 -> +0xd4
 *   branch +0x5c -> +0xa8
 *   branch +0x60 -> +0xc0
 *   branch +0x74 -> +0x88
 *   branch +0x84 -> +0x90
 *   branch +0xa4 -> +0xd4
 *   branch +0xbc -> +0xd4
 *   branch +0xc8 -> +0xd4
 *   branch +0xd8 -> +0xe8
 *   branch +0x120 -> +0x134
 *   branch +0x168 -> +0x174
 *   branch +0x198 -> +0x1a8
 *   branch +0x1b4 -> +0x21c
 *   branch +0x1ec -> +0x1fc
 *   branch +0x20c -> +0x280
 *   branch +0x218 -> +0x280
 *   branch +0x224 -> +0x240
 *   branch +0x23c -> +0x280
 *   branch +0x248 -> +0x27c
 *   branch +0x260 -> +0x270
 *   branch +0x26c -> +0x280
 *   branch +0x278 -> +0x280
 *   test +0x2c cmp r0, #0
 *   test +0x40 cmp r1, #5
 *   test +0x6c cmp r1, r0
 *   test +0x94 cmp r0, #6
 *   test +0xac cmp r0, #6
 *   test +0xd4 cmp r5, #0
 *   test +0x11c cmp r1, r0
 *   test +0x160 cmp r0, #1
 *   test +0x164 cmpne r0, #4
 *   test +0x194 cmp r0, #0
 *   test +0x1b0 cmp r0, #0
 *   test +0x1e8 cmp r0, #0
 *   test +0x204 cmp r0, #1
 *   test +0x208 cmpne r0, #4
 *   test +0x220 tst r1, #2
 *   test +0x244 tst r1, r0
 *   test +0x258 cmp r5, #1
 *   1 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ff96c; the literal pool and
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
extern void native_fn_021db438(void);
extern void native_fn_02213adc(void);
extern void native_fn_02201350(void);
extern void native_fn_021fd5fc(void);
extern void native_fn_02026144(void);
extern void native_fn_022023c4(void);
extern void native_fn_021fe3dc(void);
extern void native_fn_021fde38(void);
extern void native_fn_02203418(void);
extern void native_fn_02202420(void);
extern void native_fn_02204558(void);
extern void native_fn_021f949c(void);
extern void native_fn_02200d54(void);
extern void native_fn_02201438(void);


asm u32 native_ov001_021ff96c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    bl native_fn_0202a634
    ldr r1, =0x02239c10
    mov r6, r0
    ldrsb r0, [r1, #12]
    mov r5, #0
    bl native_fn_02202360
    ldr r1, =0x02239c10
    mov r4, r0
    ldrb r0, [r1, #0x9]
    cmp r0, #0
    beq ov001_021ff96c_L190
    ldrsb r1, [r1, #12]
    mov r0, #4
    mov r5, r0
    cmp r1, #5
    addls pc, pc, r1, lsl #2
    b ov001_021ff96c_Ld4
    b ov001_021ff96c_Ld4
    b ov001_021ff96c_L64
    b ov001_021ff96c_Lcc
    b ov001_021ff96c_Ld4
    b ov001_021ff96c_La8
    b ov001_021ff96c_Lc0
ov001_021ff96c_L64:
    ldrsb r1, [r4, #18]
    sub r0, r0, #5
    cmp r1, r0
    mov r0, #0
    beq ov001_021ff96c_L88
    bl native_fn_021db438
    ldrsb r1, [r4, #18]
    strb r1, [r4, #0x8]
    b ov001_021ff96c_L90
ov001_021ff96c_L88:
    ldrsb r1, [r4, #8]
    bl native_fn_021db438
ov001_021ff96c_L90:
    ldrb r0, [r0, #0x323]
    cmp r0, #6
    movhi r1, #6
    movls r1, r0
    and r5, r1, #255
    b ov001_021ff96c_Ld4
ov001_021ff96c_La8:
    bl native_fn_02213adc
    cmp r0, #6
    movhi r1, #6
    movls r1, r0
    and r5, r1, #255
    b ov001_021ff96c_Ld4
ov001_021ff96c_Lc0:
    mov r0, #2
    mov r5, r0
    b ov001_021ff96c_Ld4
ov001_021ff96c_Lcc:
    mov r0, #5
    mov r5, r0
ov001_021ff96c_Ld4:
    cmp r5, #0
    bne ov001_021ff96c_Le8
    bl native_fn_02201350
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
ov001_021ff96c_Le8:
    mov r1, r5, lsl #1
    add r1, r1, #2
    and r1, r1, #255
    stmia sp, {r1, r5}
    ldr r1, =0x02239c10
    str r0, [sp, #0x8]
    ldrsb r0, [r1, #12]
    mov r1, #11
    mov r2, #1
    mov r3, #21
    bl native_fn_021fd5fc
    ldr r0, [r4]
    sub r1, r5, #1
    cmp r1, r0
    bge ov001_021ff96c_L134
    mov r1, r5
    bl native_fn_02026144
    mul r0, r5, r0
    str r0, [r4, #0x4]
ov001_021ff96c_L134:
    mov r0, #140
    bl native_fn_022023c4
    ldr r1, =0x02239c10
    mov r0, #9
    ldrsb r1, [r1, #12]
    bl native_fn_021fe3dc
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_021fde38
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #1
    cmpne r0, #4
    bne ov001_021ff96c_L174
    mov r0, #256
    bl native_fn_022023c4
ov001_021ff96c_L174:
    mov r0, #2
    strb r0, [r4, #0x13]
    ldr r1, =0x02239c10
    mov r0, #0
    strb r0, [r1, #0x9]
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
ov001_021ff96c_L190:
    bl native_fn_02203418
    cmp r0, #0
    beq ov001_021ff96c_L1a8
    bl native_fn_02201350
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
ov001_021ff96c_L1a8:
    mov r0, r4
    bl native_fn_02202420
    cmp r0, #0
    beq ov001_021ff96c_L21c
    ldr r2, [r4]
    ldr r1, [r4, #0x4]
    add r0, r4, #24
    sub r1, r2, r1
    bl native_fn_02204558
    ldr r1, =0x02239c10
    mov r0, #9
    ldrsb r1, [r1, #12]
    bl native_fn_021fe3dc
    mov r0, #8
    bl native_fn_022023c4
    ldrb r0, [r4, #0x11]
    cmp r0, #0
    beq ov001_021ff96c_L1fc
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_021fde38
ov001_021ff96c_L1fc:
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    cmp r0, #1
    cmpne r0, #4
    bne ov001_021ff96c_L280
    mov r0, #256
    bl native_fn_022023c4
    b ov001_021ff96c_L280
ov001_021ff96c_L21c:
    ldrh r1, [r6, #2]
    tst r1, #2
    beq ov001_021ff96c_L240
    bl native_fn_02201350
    mov r5, r0
    mov r0, #83
    mov r1, #1
    bl native_fn_021f949c
    b ov001_021ff96c_L280
ov001_021ff96c_L240:
    ldr r0, =0x00000201
    tst r1, r0
    beq ov001_021ff96c_L27c
    ldr r0, [r4]
    bl native_fn_02200d54
    mov r5, r0
    cmp r5, #1
    mov r1, #1
    bne ov001_021ff96c_L270
    mov r0, #82
    bl native_fn_021f949c
    b ov001_021ff96c_L280
ov001_021ff96c_L270:
    mov r0, #84
    bl native_fn_021f949c
    b ov001_021ff96c_L280
ov001_021ff96c_L27c:
    bl native_fn_02201438
ov001_021ff96c_L280:
    mov r0, r5
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
