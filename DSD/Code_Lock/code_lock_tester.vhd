LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY code_lock_tester IS

	PORT (
		--INPUTS
		CLOCK_50 : IN STD_LOGIC;
		KEY : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		SW : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		--OUTPUTS
		LEDR : OUT STD_LOGIC_VECTOR(9 DOWNTO 0);
		GPIO : OUT STD_LOGIC_VECTOR(0 DOWNTO 0)
	);
END code_lock_tester;

ARCHITECTURE stuck OF code_lock_tester IS
	SIGNAL fails : STD_LOGIC_VECTOR(1 DOWNTO 0);
	SIGNAL err : STD_LOGIC_VECTOR(0 DOWNTO 0);
	SIGNAL lock_temp : STD_LOGIC;
BEGIN
	poo_poo : ENTITY work.code_lock_simple PORT MAP
		(
		clk => CLOCK_50,
		reset => KEY(0),
		enter => KEY(1),
		code => SW(3 DOWNTO 0),
		lock => LEDR(0),
		lock0 => GPIO(0),
		err_count => LEDR(9 DOWNTO 8)
		);
END stuck;