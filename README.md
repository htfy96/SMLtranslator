#Syntax of assembly file

The whole assembly program should be composed by following parts:

##;
`;` stands for the symbol of comment

##.DATA
`.DATA` indicates the beginning of data segment and declaration of variables

##Declatation of variables
Syntax:

```
VariableName Address
```

Examples:
```
X 21
Y 35
```

`VariableName` can only contain letters, numbers and _, and can't be all numbers.

##.CODE
`.CODE` stands for the beginning of code segment

##.BASE

`BASE Address` indicates the address where code segment start, and must be the next line of `.CODE`

##Statements
Here are the supported statements(case insensive):

```
;r s t stand for register from 0 to 7
;lm r,xy/var = 1RXY     Read a number from address [xy/variable] to register r                  e.g lm 3,x
;lb r,xy/var = 2RXY     Read a number [xy/variable] to register r                               e.g lb 4,15
;mov r,xy/var = 3RXY    write a number from register r to address [xy/variable]                 e.g mov 0,y
;mov r,s = 40RS         write a number from reg r to reg s                                      e.g mov 1,0
;addc r,s,t = 5RST      Complement Add r=s+t
;Addc s,t = 5SST        Another form of complement adding s=s+t
;Addf r,s,t = 6RST      Float Add r=s+t
;Addf s,t = 6SST        Another form of float adding ，s=s+t
;Or r,s,t = 7RST        Operator or r=s or t
;Or s,t = 7SST          Another form of operator or  s=s or t
;And r,s,t = 8RST       Operator and r=s and t
;And s,t = 8SST         Another form of operator and s=s and t
;Xor r,s,t = 9RST       Operator xor r=s xor t
;Xor s,t = 9SST         Another form of operator xor s=s xor t
;Rot R,X=AR0X           Circular left shift, reg r  x bits left
;J r,xy/label = BRXY    Jump by condition, if reg r=reg r0 then jump to address [xy/label]      e.g j 2,loopend
;J xy/label = B0XY      Jump by all means, jump to address [xy/label]                           e.g j 0020
;Halt = C000            Halt the program

##Label
It is disturbing to calculate address in statement `J`, then came **label**:

Write a label before a statement to mark the address of this statement:

e.g
```
label:mov 2,3
```

Then you can write
```
j 2,label
```
to directly jump to the statement

##.ENTRY
`.ENTRY 00 ; Indicate the point where program start, not implemented yet`

#About
For more details, please look up `example1.txt` as well as `example2.txt`.

Translator for Simple Machine Language by lz96@foxmail.com under MIT License.

