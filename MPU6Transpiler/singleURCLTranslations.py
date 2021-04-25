
def singleUrclTranslations() -> dict:
    return {"ADD REG REG REG": ["ADD(<A>, <B>, <C>);;"],
            "ADD REG REG IMM": ["ADD(<A>, <B>, <C>);;"],
            "ADD REG IMM REG": ["ADD(<A>, <B>, <C>);;"],
            "ADD REG IMM IMM": ["LDI(<A>, <B>);;",
                                "ADD(<A>, <A>, <C>);;"],
            
            "RSH REG REG": ["RSH(<A>, <B>);;"],
            "RSH REG IMM": ["RSH(<A>, <B>);;"],
            
            "LOD REG IMM": ["MPT(<B>) FFG();;",
                            "MOV(<A>, MR); STL(+0);"],
            "LOD REG REG": [";;",
                            "MOV(MP, <B>) FFG();;",
                            "MOV(<A>, MR); STL(+0);"],
            
            "STR IMM REG": ["MOV(MR, <B>) MPT(<A>);;"],
            "STR REG REG": ["FFG();;",
                            "MOV(MR, <B>); MOV(MP, <A>) STL(+0)"],
            "STR IMM IMM": ["MOV(MR, <B>) MPT(<A>);;"],
            "STR REG IMM": ["FFG();;",
                            "LDI(MR, <B>); LDI(MP, <A>) STL(+0)"],
            
            "JMP IMM": ["STL(<A>);;"],
            "JMP REG": ["FFG();;",
                        "STL(RP); MOV(RP, <A>) STL(+0);"],
            
            "BGE IMM REG REG": ["SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                "; STL(<A>);"],
            "BGE IMM REG IMM": ["SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                "; STL(<A>);"],
            "BGE IMM IMM REG": ["SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                "; STL(<A>);"],
            "BGE REG REG REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                "; STL(RP);"],
            "BGE REG REG IMM": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                "; STL(RP);"],
            "BGE REG IMM REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                "; STL(RP);"],
            
            "NOR REG REG REG": ["NOR(<A>, <B>, <C>);;"],
            "NOR REG REG IMM": ["NOR(<A>, <B>, <C>);;"],
            
            "SUB REG REG REG": ["SUB(<A>, <B>, <C>);;"],
            "SUB REG REG IMM": ["SUB(<A>, <B>, <C>);;"],
            "SUB REG IMM REG": ["SUB(<A>, <B>, <C>);;"],
            "SUB REG IMM IMM": ["LDI(<A>, <B>);;",
                                "SUB(<A>, <A>, <C>)"],
            
            "MOV REG REG": ["MOV(<A>, <B>);;"],
            "MOV REG IMM": ["LDI(<A>, <B>);;"],

            "IMM REG IMM": ["LDI(<A>, <B>);;"],
            
            "LSH REG REG": ["LSH(<A>, <B>);;"],
            "LSH REG IMM": ["LSH(<A>, <B>);;"],
            
            "INC REG REG": ["INC(<A>, <B>);;"],
            "INC REG IMM": ["INC(<A>, <B>);;"],
            
            "DEC REG REG": ["DEC(<A>, <B>);;"],
            "DEC REG IMM": ["DEC(<A>, <B>);;"],
            
            "NEG REG REG": ["NEG(<A>, <B>);;"],
            "NEG REG IMM": ["NEG(<A>, <B>);;"],
            
            "AND REG REG REG": ["AND(<A>, <B>);;"],
            "AND REG REG IMM": ["AND(<A>, <B>);;"],
            
            "OR REG REG IMM": ["NOR(<A>, <B>, <C>);;",
                               "NOT(<A>);;"],
            "OR REG REG IMM": ["NOR(<A>, <B>, <C>);;",
                               "NOT(<A>);;"],
            
            "NOT REG REG": ["NOT(<A>, <B>);;"],
            "NOT REG IMM": ["NOT(<A>, <B>);;"],
            
            "NAND REG REG REG": ["AND(<A>, <B>, <C>);;",
                                 "NOT(<A>);;"],
            "NAND REG REG IMM": ["AND(<A>, <B>, <C>);;",
                                 "NOT(<A>);;"],
            
            "BRL IMM REG REG": ["SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                "; STL(<A>);"],
            "BRL IMM REG IMM": ["SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                "; STL(<A>);"],
            "BRL IMM IMM REG": ["SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                "; STL(<A>);"],
            "BRL REG REG REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                "; STL(RP);"],
            "BRL REG REG IMM": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                "; STL(RP);"],
            "BRL REG IMM REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                "; STL(RP);"],
            
            "BRG IMM REG REG": ["SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                "; STL(<A>);"],
            "BRG IMM REG IMM": ["SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                "; STL(<A>);"],
            "BRG IMM IMM REG": ["SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                "; STL(<A>);"],
            "BRG REG REG REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                "; STL(RP);"],
            "BRG REG REG IMM": ["MOV(RP, <A>);;",
                                "SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                "; STL(RP);"],
            "BRG REG IMM REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                "; STL(RP);"],
            
            "BRE IMM REG REG": ["SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                "; STL(<A>);"],
            "BRE IMM REG IMM": ["SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                "; STL(<A>);"],
            "BRE IMM IMM REG": ["SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                "; STL(<A>);"],
            "BRE REG REG REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                "; STL(RP);"],
            "BRE REG REG IMM": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                "; STL(RP);"],
            "BRE REG IMM REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                "; STL(RP);"],
            
            "BNE IMM REG REG": ["SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                "; STL(<A>);"],
            "BNE IMM REG IMM": ["SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                "; STL(<A>);"],
            "BNE IMM IMM REG": ["SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                "; STL(<A>);"],
            "BNE REG REG REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                "; STL(RP);"],
            "BNE REG REG IMM": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                "; STL(RP);"],
            "BNE REG IMM REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                "; STL(RP);"],
            
            "BOD IMM REG": ["MOV(R0, <B>) FLG(OD) STL(+1);;",
                            "; STL(<A>);"],
            "BOD REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(OD) STL(+1);;",
                            "; STL(RP);"],
            
            "BEV IMM REG": ["MOV(R0, <B>) FLG(EV) STL(+1);;",
                            "; STL(<A>);"],
            "BEV REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(EV) STL(+1);;",
                            "; STL(RP);"],
            
            "BLE IMM REG REG": ["SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                "; STL(<A>);"],
            "BLE IMM REG IMM": ["SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                "; STL(<A>);"],
            "BLE IMM IMM REG": ["SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                "; STL(<A>);"],
            "BLE REG REG REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                "; STL(RP);"],
            "BLE REG REG IMM": ["MOV(RP, <A>);;",
                                "SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                "; STL(RP);"],
            "BLE REG IMM REG": ["MOV(RP, <A>);;",
                                "SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                "; STL(RP);"],
            
            "BRZ IMM REG": ["MOV(R0, <B>) FLG(ZF) STL(+1);;",
                            "; STL(<A>);"],
            "BRZ REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(ZF) STL(+1);;",
                            "; STL(RP);"],
            
            "BRZ IMM REG": ["MOV(R0, <B>) FLG(ZF) STL(+1);;",
                            "; STL(<A>);"],
            "BRZ REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(ZF) STL(+1);;",
                            "; STL(RP);"],
            
            "BZR IMM REG": ["MOV(R0, <B>) FLG(ZF) STL(+1);;",
                            "; STL(<A>);"],
            "BZR REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(ZF) STL(+1);;",
                            "; STL(RP);"],
            
            "BNZ IMM REG": ["MOV(R0, <B>) FLG(!ZF) STL(+1);;",
                            "; STL(<A>);"],
            "BNZ REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(!ZF) STL(+1);;",
                            "; STL(RP);"],
            
            "BZN IMM REG": ["MOV(R0, <B>) FLG(!ZF) STL(+1);;",
                            "; STL(<A>);"],
            "BZN REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(!ZF) STL(+1);;",
                            "; STL(RP);"],
            
            "BRN IMM REG": ["MOV(R0, <B>) FLG(NE) STL(+1);;",
                            "; STL(<A>);"],
            "BRN REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(NE) STL(+1);;",
                            "; STL(RP);"],
            
            "BRN IMM REG": ["MOV(R0, <B>) FLG(PO) STL(+1);;",
                            "; STL(<A>);"],
            "BRN REG REG": ["MOV(RP, <A>);;",
                            "MOV(R0, <B>) FLG(PO) STL(+1);;",
                            "; STL(RP);"],
            
            "PSH REG": ["INC(R10) FFG();;",
                        "MOV(MR, <A>); MOV(MP, R10) STL(+0);"],
            "PSH IMM": ["INC(R10) FFG();;",
                        "LDI(MR, <A>); MOV(MP, R10) STL(+0);"],
            
            "POP REG": ["DEC(R10) STL(+1);;",
                        "MOV(MP, R10) FFG();;",
                        "MOV(<A>, MR); STL(+0);"],
            
            "CAL IMM": ["INC(R10) FFG();;",
                        "MOV(MR, +2); MOV(MP, R10) STL(+0);",
                        "STL(<A>);;"],
            "CAL REG": ["INC(R10) FFG();;",
                        "MOV(MR, +2) FFG(); MOV(MP, R10) STL(+0);",
                        "STL(RP); MOV(RP, <A>) STL(+0);"],
            
            "RET": ["DEC(R10) STL(+1);;",
                    "MOV(MP, R10) FFG();;",
                    "MOV(RP, MR) FFG(); STL(+0);",
                    "STL(RP); STL(+0);"],
            
            "HLT": ["HLT();;"],
            
            "MLT REG REG REG": ["MOV(MR, <A>) MPT(0x21);;",
                                "MOV(MR, <B>) MPT(0x20) FFG();;",
                                "FFG(); STL(+0);",
                                "MOV(<C>, MR); STL(+0);"],
            "MLT REG REG IMM": ["MOV(MR, <A>) MPT(0x21);;",
                                "MOV(MR, <B>) MPT(0x20) FFG();;",
                                "FFG(); STL(+0);",
                                "MOV(<C>, MR); STL(+0);"],
            "MLT REG IMM REG": ["MOV(MR, <A>) MPT(0x21);;",
                                "MOV(MR, <B>) MPT(0x20) FFG();;",
                                "FFG(); STL(+0);",
                                "MOV(<C>, MR); STL(+0);"],
            
            "DIV REG REG REG": ["MOV(<A>, <B>) BRC(+2);;",
                                "MOV(CT, 253) BRC(+1);;",
                                "SUB(<A>, <A>, <C>) FLG(!CF) BRC(+0) CTI(); FFG();",
                                "; MOV(<A>, CT);"],
            "DIV REG REG IMM": ["MOV(<A>, <B>) BRC(+2);;",
                                "MOV(CT, 253) BRC(+1);;",
                                "SUB(<A>, <A>, <C>) FLG(!CF) BRC(+0) CTI(); FFG();",
                                "; MOV(<A>, CT);"],
            "DIV REG IMM REG": ["MOV(<A>, <B>) BRC(+2);;",
                                "MOV(CT, 253) BRC(+1);;",
                                "SUB(<A>, <A>, <C>) FLG(!CF) BRC(+0) CTI(); FFG();",
                                "; MOV(<A>, CT);"],
            
            "MOD REG REG REG": ["MOV(<A>, <B>) BRC(+2);;",
                                "BRC(+1);;",
                                "SUB(<A>, <A>, <C>) FLG(!CF) BRC(+0); ADD(<A>, <A>, <C>) FFG();",
                                ";;"],
            "MOD REG REG IMM": ["MOV(<A>, <B>) BRC(+2);;",
                                "BRC(+1);;",
                                "SUB(<A>, <A>, <C>) FLG(!CF) BRC(+0); ADD(<A>, <A>, <C>) FFG();",
                                ";;"],
            "MOD REG IMM REG": ["MOV(<A>, <B>) BRC(+2);;",
                                "BRC(+1);;",
                                "SUB(<A>, <A>, <C>) FLG(!CF) BRC(+0); ADD(<A>, <A>, <C>) FFG();",
                                ";;"],
            
            "BSR REG REG REG": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "RSH(<A>) STL(+0) CTD() FLG(CT);;"],
            "BSR REG REG IMM": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "RSH(<A>) STL(+0) CTD() FLG(CT);;"],
            "BSR REG IMM REG": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "RSH(<A>) STL(+0) CTD() FLG(CT);;"],
            
            "BSL REG REG REG": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "LSH(<A>) STL(+0) CTD() FLG(CT);;"],
            "BSL REG REG IMM": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "LSH(<A>) STL(+0) CTD() FLG(CT);;"],
            "BSL REG IMM REG": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "LSH(<A>) STL(+0) CTD() FLG(CT);;"],
            
            "SRS REG REG": ["RSA(<A>, <B>);;"],
            "SRS REG IMM": ["RSA(<A>, <B>);;"],
            
            "BSS REG REG REG": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "RSA(<A>) STL(+0) CTD() FLG(CT);;"],
            "BSS REG REG IMM": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "RSA(<A>) STL(+0) CTD() FLG(CT);;"],
            "BSS REG IMM REG": ["MOV(CT, <C>);;",
                                "MOV(<A>, <B>);;",
                                "RSA(<A>) STL(+0) CTD() FLG(CT);;"],
            
            "SETE REG REG REG": ["SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETE REG REG IMM": ["SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETE REG IMM REG": ["SUB(R0, <B>, <C>) FLG(ZF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETE REG IMM IMM": ["LDI(<A>, <B>);;",
                                 "SUB(R0, <A>, <C>) FLG(ZF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            
            "SETNE REG REG REG": ["SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETNE REG REG IMM": ["SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETNE REG IMM REG": ["SUB(R0, <B>, <C>) FLG(!ZF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETNE REG IMM IMM": ["LDI(<A>, <B>);;",
                                  "SUB(R0, <A>, <C>) FLG(!ZF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            
            "SETG REG REG REG": ["SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETG REG REG IMM": ["SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETG REG IMM REG": ["SUB(R0, <C>, <B>) FLG(!CF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            
            "SETL REG REG REG": ["SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETL REG REG IMM": ["SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            "SETL REG IMM REG": ["SUB(R0, <B>, <C>) FLG(!CF) STL(+1);;",
                                 "MOV(<A>, R0); INC(<A>, R0);"],
            
            "SETGE REG REG REG": ["SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETGE REG REG IMM": ["SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETGE REG IMM REG": ["SUB(R0, <B>, <C>) FLG(CF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            
            "SETLE REG REG REG": ["SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETLE REG REG IMM": ["SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            "SETLE REG IMM REG": ["SUB(R0, <C>, <B>) FLG(CF) STL(+1);;",
                                  "MOV(<A>, R0); INC(<A>, R0);"],
            
            "OUT %8SEG REG": ["MOV(MR, <B>) MPT(0x22) FFG();;",
                              "MOV(MP, 0x24); STL(+0);",
                              "MOV(MP, 0x23) RPT(+3);;",
                              "MPT(0x22) RET();;",
                              "RET();;",
                              "MOV(R0, MR) HSH();;"],
            "OUT %8SEG IMM": ["MOV(R0, <B>) HSH();;"],
            "OUT %8SEG NEWLINE": ["VSH();;"],
            "OUT %8SEG CLEAR": ["CLR();;"],
            "OUT %"+"X REG": ["MOV(R0, <B>) XXX();;"],
            "OUT %"+"X IMM": ["LDI(R0, <B>) XXX();;"],
            "OUT %Y REG": ["MOV(R0, <B>) YYY();;"],
            "OUT %Y IMM": ["LDI(R0, <B>) YYY();;"],
            "OUT PIXEL PRINT": ["PRT();;"],
            "OUT PIXEL ERASE": ["ERS();;"],
            "OUT PIXEL RESET": ["RST();;"],
            
            "IN REG %RNG": ["MPT(0x2C) FFG();;",
                           "MOV(<A>, MR); STL(+0);"],
            "IN REG %UI": ["MOV(<A>, IN);;"]
            }
    
    
    
    
    