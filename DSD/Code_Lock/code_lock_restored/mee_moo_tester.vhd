LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY mee_moo_tester IS

	PORT (
		KEY : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		SW : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		LEDR : OUT STD_LOGIC_VECTOR(1 DOWNTO 0)
	);

END mee_moo_tester;

ARCHITECTURE ko OF mee_moo_tester IS
BEGIN
	mee_moo : ENTITY work.three_process_fsm_template PORT MAP
		(
		clk => KEY(0),
		reset => KEY(1),
		a => SW(0),
		b => SW(1),
		mooout => LEDR(0),
		meeout => LEDR(1)
		);
END ko;