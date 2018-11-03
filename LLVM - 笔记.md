# The LLVM target-independent code generator consists of six main components （概述）
## 1. Abstract target description interfaces
`include/llvm/Target/`  
> Capture important properties about various aspects of the machine, independently of how they will be used.  

## 2. Classes used to represent the code being generated for a target
`include/llvm/CodeGen/`
> These classes are intended to be abstract enough to represent the machine code for any target machine.  
> At this level, concepts like “constant pool entries” and “jump tables” are explicitly exposed.  

## 3. Classes and algorithms used to represent code at the object file level, the MC Layer
> These classes represent assembly level constructs like labels, sections, and instructions.  
> At this level, concepts like “constant pool entries” and “jump tables” don’t exist.  

## 4. Target-independent algorithms
`lib/CodeGen/`
> Used to implement various phases of native code generation (register allocation, scheduling, stack frame representation, etc).  

## 5. Implementations of the abstract target description interfaces for particular targets
`lib/Target/`

## 6. JIT
`lib/ExecutionEngine/JIT`


<br>
-----
# Required components in the code generator （重点关注）
`TargetMachine` and `DataLayout` class  
> High-level interface and reusable components.  
> Are the only ones that are required to be defined for a backend to fit into the LLVM system.  
> But the others interface must be defined if the reusable code generator components are going to be used.  

> 看起来只需要定义这两个类，就可以实现出后端


<br>
-----
# The high-level design of the code generator （CodeGen 宏观步骤）
> Designed to support efficient and quality code generation for standard register-based microprocessors.  

## 1. Instruction Selection
> Determines an efficient way to express the input LLVM code in the target instruction set.  
> Produces the initial code. (in target instruction set)  
> Then makes use of SSA virtual registers and physical registers that represent any required register assignments.

> 这一步已经将 LLVM IR 转换成了 DAG  
> ？采用 SSA 的原因是由于目标物理条件限制和函数调用的规范

## 2. Scheduling and Formation
> Determines an ordering of the instructions (in DAG format).  
> Then emits the instructions as `MachineInstrs` with that ordering.

> ? It operates on a SelectionDAG

## 3. SSA-based Machine Code Optimizations
> This is an optional stage.  
> Machine-code optimizations that operate on the SSA-form.  
> Modulo-scheduling or peephole optimization work here.  
> > Modulo scheduling: an algorithm for generating software pipelining, which is a way of increasing instruction level parallelism by interleaving different iterations of an inner loop.  
>
> > Peephole optimization: a kind of optimization performed over a very small set of instructions in a segment of generated code. The set is called a "peephole" or a "window". It works by recognizing sets of instructions that can be replaced by shorter or faster sets of instructions.

## 4. Register Allocation
> Infinite virtual register file -> Concrete register file.  
> This phase introduces spill code and eliminates all virtual register references from the program.  

> ? spill code

## 5. Prolog/Epilog Code Insertion 
> Once the machine code has been generated for the function and the amount of stack space required is known.  
> Prolog and epilog code for the function can be inserted and “abstract stack location references” can be eliminated.

> 猜测：在这一步之前，各种函数调用以及变量访问都是用相对位置或者助记符来表示的。到这步以后，全部处理成绝对位置。

## 6. Late Machine Code Optimizations
> Optimizations that operate on “final” machine code.  
> Such as pill code scheduling and peephole optimizations.

## 7. Code Emission
> Final stage, puts out the code for the current function.



<br>
-----
# Hierarchies （继承关系）



