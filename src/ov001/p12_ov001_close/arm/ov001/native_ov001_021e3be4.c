/* ov001 row 0x021e3be4: 460 bytes.
 *
 * What it does: 110 instructions; 18 call(s) to 0x020656e0, 0x021f1a44, 0x021db438, +15 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 5 literal slot(s) in the extent
 *
 * Decoded shape: loop with 18 calls (110 instructions, 18 calls, 4 branches, 14 back edges, 5 literal slots).
 *
 *   pool +0x1b8 -> constant 0x02238d18 (image word 0x02238d18)
 *   pool +0x1bc -> constant 0x000f423f (image word 0x000f423f)
 *   pool +0x1c0 -> constant 0x02238cd4 (image word 0x02238cd4)
 *   pool +0x1c4 -> constant 0x3f666666 (image word 0x3f666666)
 *   pool +0x1c8 -> constant 0x0001869f (image word 0x0001869f)
 *   branch +0x0c -> +0x28
 *   branch +0x58 -> +0x84
 *   branch +0x80 -> +0x98
 *   back edge +0xa4 -> +0x3c
 *   branch +0xd0 -> +0xfc
 *   back edge +0x104 -> +0xb8
 *   test +0x08 cmp r0, #1
 *   test +0x4c cmp r1, #0
 *   test +0x54 cmpne r1, #0
 *   test +0x70 cmp r1, #0
 *   test +0x88 cmp r1, #0
 *   test +0x9c cmp r7, #3
 *   test +0xcc cmp r0, #0
 *   test +0x100 cmp r10, #3
 *   test +0x110 cmp r0, #0
 *   test +0x128 cmp r0, #0
 *   test +0x134 cmp r4, r0
 *   test +0x188 cmp r0, r1
 *   test +0x198 cmp r5, r1
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e3be4; the literal pool and
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

extern void native_fn_020656e0(void);
extern void native_fn_021f1a44(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0220f3ac(void);
extern void native_fn_0220f3f4(void);
extern void native_fn_02044424(void);
extern void native_fn_021db578(void);
extern void native_fn_02025a28(void);
extern void native_fn_02025578(void);
extern void native_fn_02024e0c(void);
extern void native_fn_020259b4(void);
extern void native_fn_0221157c(void);


asm u32 native_ov001_021e3be4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    bl native_fn_020656e0
    cmp r0, #1
    bne ov001_021e3be4_L28
    mov r0, #6
    bl native_fn_021f1a44
    mov r1, #0
    strb r1, [r0, #0x23]
    mov r0, #6
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov001_021e3be4_L28:
    mov r4, #0
    ldr r8, =0x02238d18
    mov r5, r4
    mov r7, r4
    mov r6, #1
ov001_021e3be4_L3c:
    mov r0, r6
    mov r1, r7
    bl ov001_side_slot_record_021db438
    ldrb r1, [r0, #0x31c]
    cmp r1, #0
    ldrneb r1, [r0, #0x1ff]
    cmpne r1, #0
    beq ov001_021e3be4_L84
    ldr r2, [r0, #0x1e8]
    ldr r0, [r2, #0x4]
    ldrsh r1, [r2, #48]
    add r4, r4, r0
    ldrsh r0, [r2, #40]
    cmp r1, #0
    addgt r0, r0, r1
    addgt r5, r5, r0
    addle r5, r5, r0
    b ov001_021e3be4_L98
ov001_021e3be4_L84:
    ldrb r1, [r8]
    cmp r1, #0
    ldrne r0, [r0, #0x1e8]
    ldrnesh r0, [r0, #40]
    addne r5, r5, r0
ov001_021e3be4_L98:
    add r7, r7, #1
    cmp r7, #3
    add r8, r8, #1
    blt ov001_021e3be4_L3c
    mov r10, #0
    mov r8, r4
    mov r9, r5
    mov r7, r10
ov001_021e3be4_Lb8:
    mov r0, r7
    mov r1, r10
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021e3be4_Lfc
    ldr r0, [r6, #0x1e8]
    mov r1, r8
    add r0, r0, #70
    bl native_fn_0220f3ac
    ldr r2, [r6, #0x1e8]
    add r4, r4, r0
    mov r1, r9
    add r0, r2, #70
    bl native_fn_0220f3f4
    add r5, r5, r0
ov001_021e3be4_Lfc:
    add r10, r10, #1
    cmp r10, #3
    blt ov001_021e3be4_Lb8
    mov r0, #65536
    bl native_fn_02044424
    cmp r0, #0
    movne r0, #10
    mulne r0, r5, r0
    movne r5, r0
    mov r0, #16384
    bl native_fn_02044424
    cmp r0, #0
    ldr r0, =0x000f423f
    addne r4, r4, r4, lsl #2
    cmp r4, r0
    movge r4, r0
    ldr r1, =0x02238cd4
    mov r0, #0
    str r4, [r1, #0x38]
    bl native_fn_021db578
    mov r6, r0
    mov r0, r4
    bl native_fn_02025a28
    mov r4, r0
    mov r0, r6
    bl native_fn_02025a28
    mov r1, r0
    mov r0, r4
    bl native_fn_02025578
    mov r1, r0
    ldr r0, =0x3f666666
    bl native_fn_02024e0c
    bl native_fn_020259b4
    ldr r1, =0x000f423f
    ldr r2, =0x02238cd4
    cmp r0, r1
    movge r0, r1
    ldr r1, =0x0001869f
    str r0, [r2, #0x30]
    cmp r5, r1
    movge r5, r1
    ldr r0, =0x02238cd4
    mov r1, r5
    str r5, [r0, #0x34]
    ldr r0, [r0, #0x30]
    bl native_fn_0221157c
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
