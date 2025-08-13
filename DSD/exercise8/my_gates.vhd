LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;

PACKAGE my_gates IS
  FUNCTION xor_funk(SIGNAL a, b : IN STD_LOGIC) RETURN STD_LOGIC;
  PROCEDURE find_and_or(
    a, b : IN STD_LOGIC;
    SIGNAL or_out, and_out : OUT STD_LOGIC);
END my_gates;

PACKAGE BODY my_gates IS
  -- XOR function
  FUNCTION xor_funk(SIGNAL a, b : IN STD_LOGIC) RETURN STD_LOGIC IS
  BEGIN
    RETURN a XOR b;
  END xor_funk;
  -- and or procedure
  PROCEDURE find_and_or(
    a, b : IN STD_LOGIC;
    SIGNAL or_out, and_out : OUT STD_LOGIC) IS
  BEGIN
    or_out <= a OR b;
    and_out <= a AND b;
  END find_and_or;
END my_gates;