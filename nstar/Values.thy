theory Values
  imports
    Main
    Registers
begin

datatype val =
  Vint int
| Vreg reg

end
