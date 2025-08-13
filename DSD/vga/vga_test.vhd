LIBRARY ieee;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.ALL;

ENTITY vga_test IS
	PORT (
		clock_50            : IN Std_logic;
		key0                : IN Std_logic;
		vga_hs, vga_vs      : OUT Std_logic;
		vga_b, vga_g, vga_r : OUT Std_logic_vector(3 DOWNTO 0));
END ENTITY;

ARCHITECTURE vga_test_impl OF vga_test IS

BEGIN
	
	vga_comp : ENTITY work.vga

		PORT MAP
		(
			clk   => clock_50,
			reset => key0,
			red   => vga_r,
			green => vga_g,
			blue  => vga_b,
			vsync => vga_vs,
			hsync => vga_hs
		);
END ARCHITECTURE;