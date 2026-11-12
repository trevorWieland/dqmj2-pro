/* ov006 row 0x021fd314: 260 bytes.
 *
 * What it does: 98 instructions; 21 call(s) to 0x021f5344, 0x02203fac, 0x021f23a0, +18 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, r7, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xec -> native_data_0220b900 (image word 0x0220b900)
 *   pool +0xf0 -> constant 0x0221c114 (image word 0x0221c114)
 *   pool +0xf4 -> native_data_0220b940 (image word 0x0220b940)
 *   pool +0xf8 -> native_data_0220b944 (image word 0x0220b944)
 *   pool +0xfc -> native_data_0220b942 (image word 0x0220b942)
 *   pool +0x100 -> native_data_0220b946 (image word 0x0220b946)
 *   branch +0x1c -> +0x76
 *   back edge +0x7c -> +0x0a
 *   branch +0x86 -> +0x90
 *   branch +0x98 -> +0xa2
 *   branch +0xaa -> +0xb4
 *   branch +0xbc -> +0xc6
 *   branch +0xce -> +0xd8
 *   branch +0xe0 -> +0xe8
 *   test +0x1a cmp r0, #0x0
 *   test +0x7a cmp r4, #0x4
 *   test +0x84 cmp r0, #0x0
 *   test +0x96 cmp r0, #0x0
 *   test +0xa8 cmp r0, #0x0
 *   test +0xba cmp r0, #0x0
 *   test +0xcc cmp r0, #0x0
 *   test +0xde cmp r0, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021fd314; the literal pool and
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

extern u8 native_data_0220b900[];
extern void native_fn_021f5344(void);
extern void native_fn_02203fac(void);
extern void native_fn_021f23a0(void);
extern u8 native_data_0220b940[];
extern u8 native_data_0220b944[];
extern u8 native_data_0220b942[];
extern u8 native_data_0220b946[];
extern void native_fn_021f29bc(void);
extern void native_fn_02203ebc(void);
extern void native_fn_02203eec(void);
extern void native_fn_021fd580(void);


asm u32 native_ov006_021fd314 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    mov r4, #0x0
    ldr r6, =native_data_0220b900
    add r5, r4, #0x0
    mov r7, #0x1
ov006_021fd314_La:
    add r0, r7, #0x0
    bl native_fn_021f5344
    lsl r0, r0, #0x5
    add r0, r6, r0
    add r0, r0, r5
    bl native_fn_02203fac
    cmp r0, #0x0
    beq ov006_021fd314_L76
    mov r0, #0x1
    bl native_fn_021f23a0
    ldr r0, =0x0221c114
    strb r4, [r0, #0x1]
    mov r0, #0x1
    bl native_fn_021f5344
    add r5, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    add r4, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    add r6, r0, #0x0
    mov r0, #0x1
    bl native_fn_021f5344
    lsl r1, r5, #0x5
    add r3, r0, #0x0
    ldr r0, =native_data_0220b940
    ldr r5, =0x0221c114
    mov r2, #0x1
    ldrsb r2, [r5, r2]
    add r0, r0, r1
    ldr r1, =native_data_0220b944
    lsl r5, r2, #0x3
    lsl r2, r4, #0x5
    add r1, r1, r2
    ldr r2, =native_data_0220b942
    lsl r4, r6, #0x5
    add r2, r2, r4
    lsl r4, r3, #0x5
    ldr r3, =native_data_0220b946
    ldrh r0, [r5, r0]
    add r3, r3, r4
    ldrh r1, [r5, r1]
    ldrh r2, [r5, r2]
    ldrh r3, [r5, r3]
    bl native_fn_021f29bc
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fd314_L76:
    add r4, r4, #0x1
    add r5, #0x8
    cmp r4, #0x4
    blo ov006_021fd314_La
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021fd314_L90
    mov r0, #0x1
    bl native_fn_021f23a0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fd314_L90:
    mov r0, #0x2
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq ov006_021fd314_La2
    mov r0, #0x0
    bl native_fn_021f23a0
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fd314_La2:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fd314_Lb4
    mov r0, #0x1
    bl native_fn_021fd580
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fd314_Lb4:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fd314_Lc6
    mov r0, #0x3
    bl native_fn_021fd580
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fd314_Lc6:
    mov r0, #0x20
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fd314_Ld8
    mov r0, #0x0
    bl native_fn_021fd580
    pop {r3, r4, r5, r6, r7, pc}
ov006_021fd314_Ld8:
    mov r0, #0x10
    bl native_fn_02203eec
    cmp r0, #0x0
    beq ov006_021fd314_Le8
    mov r0, #0x2
    bl native_fn_021fd580
ov006_021fd314_Le8:
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
